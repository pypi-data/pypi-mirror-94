#   Copyright 2015 Red Hat, Inc.
#
#   Licensed under the Apache License, Version 2.0 (the "License"); you may
#   not use this file except in compliance with the License. You may obtain
#   a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#   WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#   License for the specific language governing permissions and limitations
#   under the License.
#

import collections
import copy
import json
import mock
import os
import tempfile

import fixtures
from osc_lib import exceptions as oscexc
from osc_lib.tests import utils as test_utils
import yaml

from tripleoclient import exceptions
from tripleoclient.tests.v1.overcloud_node import fakes
from tripleoclient.v1 import overcloud_node


class TestDeleteNode(fakes.TestDeleteNode):

    def setUp(self):
        super(TestDeleteNode, self).setUp()

        # Get the command object to test
        self.cmd = overcloud_node.DeleteNode(self.app, None)
        self.app.client_manager.workflow_engine = mock.Mock()
        self.tripleoclient = mock.Mock()

        self.websocket = mock.Mock()
        self.websocket.__enter__ = lambda s: self.websocket
        self.websocket.__exit__ = lambda s, *exc: None
        self.tripleoclient = mock.Mock()
        self.tripleoclient.messaging_websocket.return_value = self.websocket
        self.app.client_manager.tripleoclient = self.tripleoclient

        self.workflow = self.app.client_manager.workflow_engine
        self.stack_name = self.app.client_manager.orchestration.stacks.get
        self.stack_name.return_value = mock.Mock(stack_name="overcloud")
        execution = mock.Mock()
        execution.id = "IDID"
        self.workflow.executions.create.return_value = execution

    # TODO(someone): This test does not pass with autospec=True, it should
    # probably be fixed so that it can pass with that.
    def test_node_delete(self):
        argslist = ['instance1', 'instance2', '--templates',
                    '--stack', 'overcast', '--timeout', '90', '--yes']
        verifylist = [
            ('stack', 'overcast'),
            ('nodes', ['instance1', 'instance2'])
        ]
        parsed_args = self.check_parser(self.cmd, argslist, verifylist)

        self.websocket.wait_for_messages.return_value = iter([{
            "execution_id": "IDID",
            "status": "SUCCESS",
            "message": "Success.",
        }])

        self.stack_name.return_value = mock.Mock(stack_name="overcast")

        self.cmd.take_action(parsed_args)

        # Verify
        self.workflow.executions.create.assert_called_with(
            'tripleo.scale.v1.delete_node',
            workflow_input={
                'plan_name': 'overcast',
                'nodes': ['instance1', 'instance2'],
                'timeout': 90
            })

    @mock.patch('tripleoclient.utils.prompt_user_for_confirmation',
                return_value=False)
    def test_node_delete_no_confirm(self, confirm_mock):
        argslist = ['instance1', 'instance2', '--templates',
                    '--stack', 'overcast', '--timeout', '90']
        verifylist = [
            ('stack', 'overcast'),
            ('nodes', ['instance1', 'instance2'])
        ]
        parsed_args = self.check_parser(self.cmd, argslist, verifylist)

        self.assertRaises(oscexc.CommandError,
                          self.cmd.take_action,
                          parsed_args)

    def test_node_wrong_stack(self):
        argslist = ['instance1', '--templates',
                    '--stack', 'overcast', '--yes']
        verifylist = [
            ('stack', 'overcast'),
            ('nodes', ['instance1', ])
        ]
        parsed_args = self.check_parser(self.cmd, argslist, verifylist)

        self.stack_name.return_value = None

        self.assertRaises(exceptions.InvalidConfiguration,
                          self.cmd.take_action,
                          parsed_args)

        # Verify
        self.workflow.executions.create.assert_not_called()

    def test_node_delete_without_stack(self):

        arglist = ['instance1', '--yes']

        verifylist = [
            ('stack', 'overcloud'),
            ('nodes', ['instance1']),
        ]
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        self.websocket.wait_for_messages.return_value = iter([{
            "execution_id": "IDID",
            "status": "SUCCESS",
            "message": "Success.",
        }])

        self.cmd.take_action(parsed_args)

        # Verify
        self.workflow.executions.create.assert_called_with(
            'tripleo.scale.v1.delete_node',
            workflow_input={
                'plan_name': 'overcloud',
                'nodes': ['instance1', ],
                'timeout': 240
            })

    @mock.patch('tripleoclient.workflows.scale.ansible_tear_down')
    def test_node_delete_wrong_instance(self, mock_tear_down):

        argslist = ['wrong_instance', '--templates',
                    '--stack', 'overcloud', '--yes']
        verifylist = [
            ('stack', 'overcloud'),
            ('nodes', ['wrong_instance']),
        ]
        parsed_args = self.check_parser(self.cmd, argslist, verifylist)

        self.websocket.wait_for_messages.return_value = iter([{
            "status": "FAILED",
            "execution_id": "IDID",
            "message": """Failed to run action ERROR: Couldn't find \
                following instances in stack overcloud: wrong_instance"""
        }])

        # Verify
        self.assertRaises(exceptions.InvalidConfiguration,
                          self.cmd.take_action, parsed_args)

    @mock.patch('tripleoclient.workflows.baremetal.expand_roles',
                autospec=True)
    @mock.patch('tripleoclient.workflows.baremetal.undeploy_roles',
                autospec=True)
    def test_node_delete_baremetal_deployment(self, mock_undeploy_roles,
                                              mock_expand_roles):
        self.websocket.wait_for_messages.return_value = iter([{
            "execution_id": "IDID",
            "status": "SUCCESS",
            "message": "Success.",
        }])
        bm_yaml = [{
            'name': 'Compute',
            'count': 5,
            'instances': [{
                'name': 'baremetal-2',
                'hostname': 'overcast-compute-0',
                'provisioned': False
            }],
        }, {
            'name': 'Controller',
            'count': 2,
            'instances': [{
                'name': 'baremetal-1',
                'hostname': 'overcast-controller-1',
                'provisioned': False
            }]
        }]

        expand_to_delete = {
            'instances': [{
                'name': 'baremetal-1',
                'hostname': 'overcast-controller-1'
            }, {
                'name': 'baremetal-2',
                'hostname': 'overcast-compute-0'
            }]
        }
        expand_to_translate = {
            'environment': {
                'parameter_defaults': {
                    'ComputeRemovalPolicies': [{
                        'resource_list': [0]
                    }],
                    'ControllerRemovalPolicies': [{
                        'resource_list': [1]
                    }]
                }
            }
        }
        mock_expand_roles.side_effect = [
            expand_to_delete,
            expand_to_translate
        ]

        self.stack_name.return_value = mock.Mock(stack_name="overcast")
        res_list = self.app.client_manager.orchestration.resources.list
        res_list.return_value = [
            mock.Mock(
                resource_type='OS::TripleO::ComputeServer',
                parent_resource='0',
                physical_resource_id='aaaa'
            ),
            mock.Mock(
                resource_type='OS::TripleO::ComputeServer',
                parent_resource='1',
                physical_resource_id='bbbb'
            ),
            mock.Mock(
                resource_type='OS::TripleO::ControllerServer',
                parent_resource='0',
                physical_resource_id='cccc'
            ),
            mock.Mock(
                resource_type='OS::TripleO::ControllerServer',
                parent_resource='1',
                physical_resource_id='dddd'
            ),
            mock.Mock(
                resource_type='OS::TripleO::ControllerServer',
                parent_resource='2',
                physical_resource_id='eeee'
            )
        ]

        with tempfile.NamedTemporaryFile(mode='w') as inp:
            yaml.dump(bm_yaml, inp, encoding='utf-8')
            inp.flush()

            argslist = ['--baremetal-deployment', inp.name, '--templates',
                        '--stack', 'overcast', '--timeout', '90', '--yes']
            verifylist = [
                ('stack', 'overcast'),
                ('baremetal_deployment', inp.name)
            ]
            parsed_args = self.check_parser(self.cmd, argslist, verifylist)

            self.cmd.take_action(parsed_args)

        # Verify
        res_list.assert_called_once_with('overcast', nested_depth=5)
        mock_expand_roles.assert_has_calls([
            mock.call(
                self.app.client_manager,
                provisioned=False,
                roles=bm_yaml,
                stackname='overcast'
            ),
            mock.call(
                self.app.client_manager,
                provisioned=True,
                roles=bm_yaml,
                stackname='overcast'
            )
        ])
        self.workflow.executions.create.assert_called_with(
            'tripleo.scale.v1.delete_node',
            workflow_input={
                'plan_name': 'overcast',
                'nodes': ['aaaa', 'dddd'],
                'timeout': 90
            })
        mock_undeploy_roles.assert_called_once_with(
            self.app.client_manager,
            roles=bm_yaml,
            plan='overcast'
        )

    @mock.patch('tripleoclient.workflows.baremetal.expand_roles',
                autospec=True)
    def test_nodes_to_delete(self, mock_expand_roles):
        bm_yaml = [{
            'name': 'Compute',
            'count': 5,
            'instances': [{
                'name': 'baremetal-2',
                'hostname': 'overcast-compute-0',
                'provisioned': False
            }],
        }, {
            'name': 'Controller',
            'count': 2,
            'instances': [{
                'name': 'baremetal-1',
                'hostname': 'overcast-controller-1',
                'provisioned': False
            }]
        }]
        mock_expand_roles.return_value = {
            'instances': [{
                'name': 'baremetal-1',
                'hostname': 'overcast-controller-1'
            }, {
                'name': 'baremetal-2',
                'hostname': 'overcast-compute-0'
            }]
        }
        argslist = ['--baremetal-deployment', '/foo/bm_deploy.yaml']
        verifylist = [
            ('baremetal_deployment', '/foo/bm_deploy.yaml')
        ]
        parsed_args = self.check_parser(self.cmd, argslist, verifylist)
        result = self.cmd._nodes_to_delete(parsed_args, bm_yaml)
        expected = '''+-----------------------+-------------+
| hostname              | name        |
+-----------------------+-------------+
| overcast-controller-1 | baremetal-1 |
| overcast-compute-0    | baremetal-2 |
+-----------------------+-------------+
'''
        self.assertEqual(expected, result)

    @mock.patch('tripleoclient.workflows.baremetal.expand_roles',
                autospec=True)
    def test_translate_nodes_to_resources(self, mock_expand_roles):
        bm_yaml = [{
            'name': 'Compute',
            'count': 5,
            'instances': [{
                'name': 'baremetal-2',
                'hostname': 'overcast-compute-0',
                'provisioned': False
            }],
        }, {
            'name': 'Controller',
            'count': 2,
            'instances': [{
                'name': 'baremetal-1',
                'hostname': 'overcast-controller-1',
                'provisioned': False
            }]
        }]

        res_list = self.app.client_manager.orchestration.resources.list
        res_list.return_value = [
            mock.Mock(
                resource_type='OS::TripleO::ComputeServer',
                parent_resource='0',
                physical_resource_id='aaaa'
            ),
            mock.Mock(
                resource_type='OS::TripleO::ComputeServer',
                parent_resource='1',
                physical_resource_id='bbbb'
            ),
            mock.Mock(
                resource_type='OS::TripleO::ControllerServer',
                parent_resource='0',
                physical_resource_id='cccc'
            ),
            mock.Mock(
                resource_type='OS::TripleO::ControllerServer',
                parent_resource='1',
                physical_resource_id='dddd'
            ),
            mock.Mock(
                resource_type='OS::TripleO::ControllerServer',
                parent_resource='2',
                physical_resource_id='eeee'
            )
        ]

        mock_expand_roles.return_value = {
            'environment': {
                'parameter_defaults': {
                    'ComputeRemovalPolicies': [{
                        'resource_list': [0]
                    }],
                    'ControllerRemovalPolicies': [{
                        'resource_list': [1]
                    }]
                }
            }
        }

        argslist = ['--baremetal-deployment', '/foo/bm_deploy.yaml']
        verifylist = [
            ('baremetal_deployment', '/foo/bm_deploy.yaml')
        ]
        parsed_args = self.check_parser(self.cmd, argslist, verifylist)
        result = self.cmd._translate_nodes_to_resources(
            parsed_args, bm_yaml)
        self.assertEqual(['aaaa', 'dddd'], result)

    def test_check_skiplist_exists(self):
        mock_warning = mock.MagicMock()
        mock_log = mock.MagicMock()
        mock_log.warning = mock_warning
        env = {'parameter_defaults': {}}

        old_logger = self.cmd.log
        self.cmd.log = mock_log
        self.cmd._check_skiplist_exists(env)
        self.cmd.log = old_logger
        mock_warning.assert_not_called()

    def test_check_skiplist_exists_empty(self):
        mock_warning = mock.MagicMock()
        mock_log = mock.MagicMock()
        mock_log.warning = mock_warning
        env = {'parameter_defaults': {'DeploymentServerBlacklist': []}}

        old_logger = self.cmd.log
        self.cmd.log = mock_log
        self.cmd._check_skiplist_exists(env)
        self.cmd.log = old_logger
        mock_warning.assert_not_called()

    def test_check_skiplist_exists_warns(self):
        mock_warning = mock.MagicMock()
        mock_log = mock.MagicMock()
        mock_log.warning = mock_warning
        env = {'parameter_defaults': {'DeploymentServerBlacklist': ['a']}}

        old_logger = self.cmd.log
        self.cmd.log = mock_log
        self.cmd._check_skiplist_exists(env)
        self.cmd.log = old_logger
        expected_message = ('[WARNING] DeploymentServerBlacklist is ignored '
                            'when executing scale down actions. If the '
                            'node(s) being removed should *NOT* have any '
                            'actions executed on them, please shut them off '
                            'prior to their removal.')
        mock_warning.assert_called_once_with(expected_message)


class TestProvideNode(fakes.TestOvercloudNode):

    def setUp(self):
        super(TestProvideNode, self).setUp()

        self.workflow = self.app.client_manager.workflow_engine
        execution = mock.Mock()
        execution.id = "IDID"
        self.workflow.executions.create.return_value = execution
        client = self.app.client_manager.tripleoclient
        self.websocket = client.messaging_websocket()

        # Get the command object to test
        self.cmd = overcloud_node.ProvideNode(self.app, None)

        self.websocket.wait_for_messages.return_value = iter([{
            "status": "SUCCESS",
            "message": "Success",
            "execution_id": "IDID"
        }])

    def test_provide_all_manageable_nodes(self):

        parsed_args = self.check_parser(self.cmd,
                                        ['--all-manageable'],
                                        [('all_manageable', True)])
        self.cmd.take_action(parsed_args)

        self.workflow.executions.create.assert_called_once_with(
            'tripleo.baremetal.v1.provide_manageable_nodes',
            workflow_input={}
        )

    def test_provide_one_node(self):
        node_id = 'node_uuid1'

        parsed_args = self.check_parser(self.cmd,
                                        [node_id],
                                        [('node_uuids', [node_id])])
        self.cmd.take_action(parsed_args)

        self.workflow.executions.create.assert_called_once_with(
            'tripleo.baremetal.v1.provide',
            workflow_input={'node_uuids': [node_id]}
        )

    def test_provide_multiple_nodes(self):
        node_id1 = 'node_uuid1'
        node_id2 = 'node_uuid2'

        argslist = [node_id1, node_id2]
        verifylist = [('node_uuids', [node_id1, node_id2])]

        parsed_args = self.check_parser(self.cmd, argslist, verifylist)
        self.cmd.take_action(parsed_args)

        self.workflow.executions.create.assert_called_once_with(
            'tripleo.baremetal.v1.provide', workflow_input={
                'node_uuids': [node_id1, node_id2]
            }
        )

    def test_provide_no_node_or_flag_specified(self):
        self.assertRaises(test_utils.ParserException,
                          self.check_parser,
                          self.cmd, [], [])

    def test_provide_uuids_and_all_both_specified(self):
        argslist = ['node_id1', 'node_id2', '--all-manageable']
        verifylist = [('node_uuids', ['node_id1', 'node_id2']),
                      ('all_manageable', True)]
        self.assertRaises(test_utils.ParserException,
                          self.check_parser,
                          self.cmd, argslist, verifylist)


class TestIntrospectNode(fakes.TestOvercloudNode):

    def setUp(self):
        super(TestIntrospectNode, self).setUp()

        self.workflow = self.app.client_manager.workflow_engine
        execution = mock.Mock()
        execution.id = "IDID"
        self.workflow.executions.create.return_value = execution
        client = self.app.client_manager.tripleoclient
        self.websocket = client.messaging_websocket()

        # Get the command object to test
        self.cmd = overcloud_node.IntrospectNode(self.app, None)

    def _check_introspect_all_manageable(self, parsed_args, provide=False):
        self.websocket.wait_for_messages.return_value = iter([{
            "status": "SUCCESS",
            "message": "Success",
            "introspected_nodes": {},
            "execution_id": "IDID"
        }] * 2)

        self.cmd.take_action(parsed_args)

        call_list = [mock.call(
            'tripleo.baremetal.v1.introspect_manageable_nodes',
            workflow_input={'run_validations': False, 'concurrency': 20}
        )]

        if provide:
            call_list.append(mock.call(
                'tripleo.baremetal.v1.provide_manageable_nodes',
                workflow_input={}
            ))

        self.workflow.executions.create.assert_has_calls(call_list)
        self.assertEqual(self.workflow.executions.create.call_count,
                         2 if provide else 1)

    def _check_introspect_nodes(self, parsed_args, nodes, provide=False):
        self.websocket.wait_for_messages.return_value = [{
            "status": "SUCCESS",
            "message": "Success",
            "execution_id": "IDID",
        }]

        self.cmd.take_action(parsed_args)

        call_list = [mock.call(
            'tripleo.baremetal.v1.introspect', workflow_input={
                'node_uuids': nodes,
                'run_validations': False,
                'concurrency': 20}
        )]

        if provide:
            call_list.append(mock.call(
                'tripleo.baremetal.v1.provide', workflow_input={
                    'node_uuids': nodes}
            ))

        self.workflow.executions.create.assert_has_calls(call_list)
        self.assertEqual(self.workflow.executions.create.call_count,
                         2 if provide else 1)

    def test_introspect_all_manageable_nodes_without_provide(self):
        parsed_args = self.check_parser(self.cmd,
                                        ['--all-manageable'],
                                        [('all_manageable', True)])
        self._check_introspect_all_manageable(parsed_args, provide=False)

    def test_introspect_all_manageable_nodes_with_provide(self):
        parsed_args = self.check_parser(self.cmd,
                                        ['--all-manageable', '--provide'],
                                        [('all_manageable', True),
                                         ('provide', True)])
        self._check_introspect_all_manageable(parsed_args, provide=True)

    def test_introspect_nodes_without_provide(self):
        nodes = ['node_uuid1', 'node_uuid2']
        parsed_args = self.check_parser(self.cmd,
                                        nodes,
                                        [('node_uuids', nodes)])
        self._check_introspect_nodes(parsed_args, nodes, provide=False)

    def test_introspect_nodes_with_provide(self):
        nodes = ['node_uuid1', 'node_uuid2']
        argslist = nodes + ['--provide']

        parsed_args = self.check_parser(self.cmd,
                                        argslist,
                                        [('node_uuids', nodes),
                                         ('provide', True)])
        self._check_introspect_nodes(parsed_args, nodes, provide=True)

    def test_introspect_no_node_or_flag_specified(self):
        self.assertRaises(test_utils.ParserException,
                          self.check_parser,
                          self.cmd, [], [])

    def test_introspect_uuids_and_all_both_specified(self):
        argslist = ['node_id1', 'node_id2', '--all-manageable']
        verifylist = [('node_uuids', ['node_id1', 'node_id2']),
                      ('all_manageable', True)]
        self.assertRaises(test_utils.ParserException,
                          self.check_parser,
                          self.cmd, argslist, verifylist)


class TestCleanNode(fakes.TestOvercloudNode):

    def setUp(self):
        super(TestCleanNode, self).setUp()

        self.workflow = self.app.client_manager.workflow_engine
        execution = mock.Mock()
        execution.id = "IDID"
        self.workflow.executions.create.return_value = execution
        client = self.app.client_manager.tripleoclient
        self.websocket = client.messaging_websocket()

        # Get the command object to test
        self.cmd = overcloud_node.CleanNode(self.app, None)

    def _check_clean_all_manageable(self, parsed_args, provide=False):
        self.websocket.wait_for_messages.return_value = iter([{
            "status": "SUCCESS",
            "message": "Success",
            "cleaned_nodes": {},
            "execution_id": "IDID"
        }] * 2)

        self.cmd.take_action(parsed_args)

        call_list = [mock.call(
            'tripleo.baremetal.v1.clean_manageable_nodes',
            workflow_input={}
        )]

        if provide:
            call_list.append(mock.call(
                'tripleo.baremetal.v1.provide_manageable_nodes',
                workflow_input={}
            ))

        self.workflow.executions.create.assert_has_calls(call_list)
        self.assertEqual(self.workflow.executions.create.call_count,
                         2 if provide else 1)

    def _check_clean_nodes(self, parsed_args, nodes, provide=False):
        self.websocket.wait_for_messages.return_value = [{
            "status": "SUCCESS",
            "message": "Success",
            "execution_id": "IDID"
        }]

        self.cmd.take_action(parsed_args)

        call_list = [mock.call(
            'tripleo.baremetal.v1.clean_nodes', workflow_input={
                'node_uuids': nodes}
        )]

        if provide:
            call_list.append(mock.call(
                'tripleo.baremetal.v1.provide', workflow_input={
                    'node_uuids': nodes}
            ))

        self.workflow.executions.create.assert_has_calls(call_list)
        self.assertEqual(self.workflow.executions.create.call_count,
                         2 if provide else 1)

    def test_clean_all_manageable_nodes_without_provide(self):
        parsed_args = self.check_parser(self.cmd,
                                        ['--all-manageable'],
                                        [('all_manageable', True)])
        self._check_clean_all_manageable(parsed_args, provide=False)

    def test_clean_all_manageable_nodes_with_provide(self):
        parsed_args = self.check_parser(self.cmd,
                                        ['--all-manageable', '--provide'],
                                        [('all_manageable', True),
                                         ('provide', True)])
        self._check_clean_all_manageable(parsed_args, provide=True)

    def test_clean_nodes_without_provide(self):
        nodes = ['node_uuid1', 'node_uuid2']
        parsed_args = self.check_parser(self.cmd,
                                        nodes,
                                        [('node_uuids', nodes)])
        self._check_clean_nodes(parsed_args, nodes, provide=False)

    def test_clean_nodes_with_provide(self):
        nodes = ['node_uuid1', 'node_uuid2']
        argslist = nodes + ['--provide']

        parsed_args = self.check_parser(self.cmd,
                                        argslist,
                                        [('node_uuids', nodes),
                                         ('provide', True)])
        self._check_clean_nodes(parsed_args, nodes, provide=True)


class TestImportNode(fakes.TestOvercloudNode):

    def setUp(self):
        super(TestImportNode, self).setUp()

        self.nodes_list = [{
            "pm_user": "stack",
            "pm_addr": "192.168.122.1",
            "pm_password": "KEY1",
            "pm_type": "pxe_ssh",
            "mac": [
                "00:0b:d0:69:7e:59"
            ],
        }, {
            "pm_user": "stack",
            "pm_addr": "192.168.122.2",
            "pm_password": "KEY2",
            "pm_type": "pxe_ssh",
            "mac": [
                "00:0b:d0:69:7e:58"
            ]
        }]
        self.json_file = tempfile.NamedTemporaryFile(
            mode='w', delete=False, suffix='.json')
        json.dump(self.nodes_list, self.json_file)
        self.json_file.close()
        self.addCleanup(os.unlink, self.json_file.name)

        self.workflow = self.app.client_manager.workflow_engine
        execution = mock.Mock()
        execution.id = "IDID"
        self.workflow.executions.create.return_value = execution
        client = self.app.client_manager.tripleoclient
        self.websocket = client.messaging_websocket()

        # Get the command object to test
        self.cmd = overcloud_node.ImportNode(self.app, None)

        image = collections.namedtuple('image', ['id', 'name'])
        self.app.client_manager.image = mock.Mock()
        self.app.client_manager.image.images.list.return_value = [
            image(id=3, name='overcloud-full'),
        ]

        self.http_boot = '/var/lib/ironic/httpboot'

        self.useFixture(fixtures.MockPatch(
            'os.path.exists', autospec=True,
            side_effect=lambda path: path in [os.path.join(self.http_boot, i)
                                              for i in ('agent.kernel',
                                                        'agent.ramdisk')]))

    def _check_workflow_call(self, parsed_args, introspect=False,
                             provide=False, local=None, no_deploy_image=False):
        self.websocket.wait_for_messages.return_value = [{
            "status": "SUCCESS",
            "message": "Success",
            "registered_nodes": [{
                "uuid": "MOCK_NODE_UUID"
            }],
            "execution_id": "IDID"
        }]

        self.cmd.take_action(parsed_args)

        nodes_list = copy.deepcopy(self.nodes_list)
        if not no_deploy_image:
            for node in nodes_list:
                node.update({
                    'kernel_id': 'file://%s/agent.kernel' % self.http_boot,
                    'ramdisk_id': 'file://%s/agent.ramdisk' % self.http_boot,
                })

        call_count = 1
        call_list = [mock.call(
            'tripleo.baremetal.v1.register_or_update', workflow_input={
                'nodes_json': nodes_list,
                'instance_boot_option': ('local' if local is True else
                                         'netboot' if local is False else None)
            }
        )]

        if introspect:
            call_count += 1
            call_list.append(mock.call(
                'tripleo.baremetal.v1.introspect', workflow_input={
                    'node_uuids': ['MOCK_NODE_UUID'],
                    'run_validations': False,
                    'concurrency': 20}
            ))

        if provide:
            call_count += 1
            call_list.append(mock.call(
                'tripleo.baremetal.v1.provide', workflow_input={
                    'node_uuids': ['MOCK_NODE_UUID']
                }
            ))

        self.workflow.executions.create.assert_has_calls(call_list)
        self.assertEqual(self.workflow.executions.create.call_count,
                         call_count)

    def test_import_only(self):
        argslist = [self.json_file.name]
        verifylist = [('introspect', False),
                      ('provide', False)]

        parsed_args = self.check_parser(self.cmd, argslist, verifylist)
        self._check_workflow_call(parsed_args)

    def test_import_and_introspect(self):
        argslist = [self.json_file.name, '--introspect']
        verifylist = [('introspect', True),
                      ('provide', False)]

        parsed_args = self.check_parser(self.cmd, argslist, verifylist)
        self._check_workflow_call(parsed_args, introspect=True)

    def test_import_and_provide(self):
        argslist = [self.json_file.name, '--provide']
        verifylist = [('introspect', False),
                      ('provide', True)]

        parsed_args = self.check_parser(self.cmd, argslist, verifylist)
        self._check_workflow_call(parsed_args, provide=True)

    def test_import_and_introspect_and_provide(self):
        argslist = [self.json_file.name, '--introspect', '--provide']
        verifylist = [('introspect', True),
                      ('provide', True)]

        parsed_args = self.check_parser(self.cmd, argslist, verifylist)
        self._check_workflow_call(parsed_args, introspect=True, provide=True)

    def test_import_with_netboot(self):
        arglist = [self.json_file.name, '--instance-boot-option', 'netboot']
        verifylist = [('instance_boot_option', 'netboot')]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        self._check_workflow_call(parsed_args, local=False)

    def test_import_with_no_deployed_image(self):
        arglist = [self.json_file.name, '--no-deploy-image']
        verifylist = [('no_deploy_image', True)]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        self._check_workflow_call(parsed_args, no_deploy_image=True)


class TestImportNodeMultiArch(fakes.TestOvercloudNode):

    def setUp(self):
        super(TestImportNodeMultiArch, self).setUp()

        self.nodes_list = [{
            "pm_user": "stack",
            "pm_addr": "192.168.122.1",
            "pm_password": "KEY1",
            "pm_type": "pxe_ssh",
            "mac": [
                "00:0b:d0:69:7e:59"
            ],
        }, {
            "pm_user": "stack",
            "pm_addr": "192.168.122.2",
            "pm_password": "KEY2",
            "pm_type": "pxe_ssh",
            "arch": "x86_64",
            "mac": [
                "00:0b:d0:69:7e:58"
            ]
        }, {
            "pm_user": "stack",
            "pm_addr": "192.168.122.3",
            "pm_password": "KEY3",
            "pm_type": "pxe_ssh",
            "arch": "x86_64",
            "platform": "SNB",
            "mac": [
                "00:0b:d0:69:7e:58"
            ]
        }]
        self.json_file = tempfile.NamedTemporaryFile(
            mode='w', delete=False, suffix='.json')
        json.dump(self.nodes_list, self.json_file)
        self.json_file.close()
        self.addCleanup(os.unlink, self.json_file.name)

        self.workflow = self.app.client_manager.workflow_engine
        execution = mock.Mock()
        execution.id = "IDID"
        self.workflow.executions.create.return_value = execution
        client = self.app.client_manager.tripleoclient
        self.websocket = client.messaging_websocket()

        # Get the command object to test
        self.cmd = overcloud_node.ImportNode(self.app, None)

        image = collections.namedtuple('image', ['id', 'name'])
        self.app.client_manager.image = mock.Mock()
        self.app.client_manager.image.images.list.return_value = [
            image(id=3, name='overcloud-full'),
            image(id=6, name='x86_64-overcloud-full'),
            image(id=9, name='SNB-x86_64-overcloud-full'),
        ]

        self.http_boot = '/var/lib/ironic/httpboot'

        existing = ['agent', 'x86_64/agent', 'SNB-x86_64/agent']
        existing = {os.path.join(self.http_boot, name + ext)
                    for name in existing for ext in ('.kernel', '.ramdisk')}

        self.useFixture(fixtures.MockPatch(
            'os.path.exists', autospec=True,
            side_effect=lambda path: path in existing))

    def _check_workflow_call(self, parsed_args, introspect=False,
                             provide=False, local=None, no_deploy_image=False):
        self.websocket.wait_for_messages.return_value = [{
            "status": "SUCCESS",
            "message": "Success",
            "registered_nodes": [{
                "uuid": "MOCK_NODE_UUID"
            }],
            "execution_id": "IDID"
        }]

        self.cmd.take_action(parsed_args)

        nodes_list = copy.deepcopy(self.nodes_list)
        if not no_deploy_image:
            nodes_list[0]['kernel_id'] = (
                'file://%s/agent.kernel' % self.http_boot)
            nodes_list[0]['ramdisk_id'] = (
                'file://%s/agent.ramdisk' % self.http_boot)
            nodes_list[1]['kernel_id'] = (
                'file://%s/x86_64/agent.kernel' % self.http_boot)
            nodes_list[1]['ramdisk_id'] = (
                'file://%s/x86_64/agent.ramdisk' % self.http_boot)
            nodes_list[2]['kernel_id'] = (
                'file://%s/SNB-x86_64/agent.kernel' % self.http_boot)
            nodes_list[2]['ramdisk_id'] = (
                'file://%s/SNB-x86_64/agent.ramdisk' % self.http_boot)

        call_count = 1
        call_list = [mock.call(
            'tripleo.baremetal.v1.register_or_update', workflow_input={
                'nodes_json': nodes_list,
                'instance_boot_option': ('local' if local is True else
                                         'netboot' if local is False else None)
            }
        )]

        if introspect:
            call_count += 1
            call_list.append(mock.call(
                'tripleo.baremetal.v1.introspect', workflow_input={
                    'node_uuids': ['MOCK_NODE_UUID'],
                    'run_validations': False,
                    'concurrency': 20}
            ))

        if provide:
            call_count += 1
            call_list.append(mock.call(
                'tripleo.baremetal.v1.provide', workflow_input={
                    'node_uuids': ['MOCK_NODE_UUID']
                }
            ))

        self.workflow.executions.create.assert_has_calls(call_list)
        self.assertEqual(self.workflow.executions.create.call_count,
                         call_count)

    def test_import_only(self):
        argslist = [self.json_file.name]
        verifylist = [('introspect', False),
                      ('provide', False)]

        parsed_args = self.check_parser(self.cmd, argslist, verifylist)
        self._check_workflow_call(parsed_args)

    def test_import_and_introspect(self):
        argslist = [self.json_file.name, '--introspect']
        verifylist = [('introspect', True),
                      ('provide', False)]

        parsed_args = self.check_parser(self.cmd, argslist, verifylist)
        self._check_workflow_call(parsed_args, introspect=True)

    def test_import_and_provide(self):
        argslist = [self.json_file.name, '--provide']
        verifylist = [('introspect', False),
                      ('provide', True)]

        parsed_args = self.check_parser(self.cmd, argslist, verifylist)
        self._check_workflow_call(parsed_args, provide=True)

    def test_import_and_introspect_and_provide(self):
        argslist = [self.json_file.name, '--introspect', '--provide']
        verifylist = [('introspect', True),
                      ('provide', True)]

        parsed_args = self.check_parser(self.cmd, argslist, verifylist)
        self._check_workflow_call(parsed_args, introspect=True, provide=True)

    def test_import_with_netboot(self):
        arglist = [self.json_file.name, '--instance-boot-option', 'netboot']
        verifylist = [('instance_boot_option', 'netboot')]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        self._check_workflow_call(parsed_args, local=False)

    def test_import_with_no_deployed_image(self):
        arglist = [self.json_file.name, '--no-deploy-image']
        verifylist = [('no_deploy_image', True)]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        self._check_workflow_call(parsed_args, no_deploy_image=True)


class TestConfigureNode(fakes.TestOvercloudNode):

    def setUp(self):
        super(TestConfigureNode, self).setUp()

        self.workflow = self.app.client_manager.workflow_engine
        execution = mock.Mock()
        execution.id = "IDID"
        self.workflow.executions.create.return_value = execution
        client = self.app.client_manager.tripleoclient
        self.websocket = client.messaging_websocket()
        self.websocket.wait_for_messages.return_value = iter([{
            "status": "SUCCESS",
            "message": "",
            "execution_id": "IDID"
        }])

        # Get the command object to test
        self.cmd = overcloud_node.ConfigureNode(self.app, None)

        self.http_boot = '/var/lib/ironic/httpboot'

        self.workflow_input = {
            'kernel_name': 'file://%s/agent.kernel' % self.http_boot,
            'ramdisk_name': 'file://%s/agent.ramdisk' % self.http_boot,
            'instance_boot_option': None,
            'root_device': None,
            'root_device_minimum_size': 4,
            'overwrite_root_device_hints': False
        }

    def test_configure_all_manageable_nodes(self):
        parsed_args = self.check_parser(self.cmd,
                                        ['--all-manageable'],
                                        [('all_manageable', True)])
        self.cmd.take_action(parsed_args)

        self.workflow.executions.create.assert_called_once_with(
            'tripleo.baremetal.v1.configure_manageable_nodes',
            workflow_input=self.workflow_input
        )

    def test_failed_to_configure_all_manageable_nodes(self):
        self.websocket.wait_for_messages.return_value = iter([{
            "status": "FAILED",
            "message": "Test failure.",
            "execution_id": "IDID"
        }])

        parsed_args = self.check_parser(self.cmd, ['--all-manageable'], [])
        self.assertRaises(exceptions.NodeConfigurationError,
                          self.cmd.take_action, parsed_args)

        self.workflow.executions.create.assert_called_once_with(
            'tripleo.baremetal.v1.configure_manageable_nodes',
            workflow_input=self.workflow_input
        )

    def test_configure_specified_nodes(self):
        argslist = ['node_uuid1', 'node_uuid2']
        verifylist = [('node_uuids', ['node_uuid1', 'node_uuid2'])]

        parsed_args = self.check_parser(self.cmd, argslist, verifylist)
        self.cmd.take_action(parsed_args)

        self.workflow_input['node_uuids'] = ['node_uuid1', 'node_uuid2']
        self.workflow.executions.create.assert_called_once_with(
            'tripleo.baremetal.v1.configure',
            workflow_input=self.workflow_input
        )

    def test_failed_to_configure_specified_nodes(self):
        self.websocket.wait_for_messages.return_value = iter([{
            "status": "FAILED",
            "message": "Test failure.",
            "execution_id": "IDID"
        }])

        parsed_args = self.check_parser(self.cmd, ['node_uuid1'], [])
        self.assertRaises(exceptions.NodeConfigurationError,
                          self.cmd.take_action, parsed_args)

        self.workflow_input['node_uuids'] = ['node_uuid1']
        self.workflow.executions.create.assert_called_once_with(
            'tripleo.baremetal.v1.configure',
            workflow_input=self.workflow_input
        )

    def test_configure_no_node_or_flag_specified(self):
        self.assertRaises(test_utils.ParserException,
                          self.check_parser,
                          self.cmd, [], [])

    def test_configure_uuids_and_all_both_specified(self):
        argslist = ['node_id1', 'node_id2', '--all-manageable']
        verifylist = [('node_uuids', ['node_id1', 'node_id2']),
                      ('all_manageable', True)]
        self.assertRaises(test_utils.ParserException,
                          self.check_parser,
                          self.cmd, argslist, verifylist)

    def test_configure_kernel_and_ram(self):
        argslist = ['--all-manageable', '--deploy-ramdisk', 'test_ramdisk',
                    '--deploy-kernel', 'test_kernel']
        verifylist = [('deploy_kernel', 'test_kernel'),
                      ('deploy_ramdisk', 'test_ramdisk')]

        parsed_args = self.check_parser(self.cmd, argslist, verifylist)
        self.cmd.take_action(parsed_args)

        self.workflow_input['kernel_name'] = 'test_kernel'
        self.workflow_input['ramdisk_name'] = 'test_ramdisk'
        self.workflow.executions.create.assert_called_once_with(
            'tripleo.baremetal.v1.configure_manageable_nodes',
            workflow_input=self.workflow_input
        )

    def test_configure_instance_boot_option(self):
        argslist = ['--all-manageable', '--instance-boot-option', 'netboot']
        verifylist = [('instance_boot_option', 'netboot')]

        parsed_args = self.check_parser(self.cmd, argslist, verifylist)
        self.cmd.take_action(parsed_args)

        self.workflow_input['instance_boot_option'] = 'netboot'
        self.workflow.executions.create.assert_called_once_with(
            'tripleo.baremetal.v1.configure_manageable_nodes',
            workflow_input=self.workflow_input
        )

    def test_configure_root_device(self):
        argslist = ['--all-manageable',
                    '--root-device', 'smallest',
                    '--root-device-minimum-size', '2',
                    '--overwrite-root-device-hints']
        verifylist = [('root_device', 'smallest'),
                      ('root_device_minimum_size', 2),
                      ('overwrite_root_device_hints', True)]

        parsed_args = self.check_parser(self.cmd, argslist, verifylist)
        self.cmd.take_action(parsed_args)

        self.workflow_input['root_device'] = 'smallest'
        self.workflow_input['root_device_minimum_size'] = 2
        self.workflow_input['overwrite_root_device_hints'] = True
        self.workflow.executions.create.assert_called_once_with(
            'tripleo.baremetal.v1.configure_manageable_nodes',
            workflow_input=self.workflow_input
        )

    def test_configure_specified_node_with_all_arguments(self):
        argslist = ['node_id',
                    '--deploy-kernel', 'test_kernel',
                    '--deploy-ramdisk', 'test_ramdisk',
                    '--instance-boot-option', 'netboot',
                    '--root-device', 'smallest',
                    '--root-device-minimum-size', '2',
                    '--overwrite-root-device-hints']
        verifylist = [('node_uuids', ['node_id']),
                      ('deploy_kernel', 'test_kernel'),
                      ('deploy_ramdisk', 'test_ramdisk'),
                      ('instance_boot_option', 'netboot'),
                      ('root_device', 'smallest'),
                      ('root_device_minimum_size', 2),
                      ('overwrite_root_device_hints', True)]

        parsed_args = self.check_parser(self.cmd, argslist, verifylist)
        self.cmd.take_action(parsed_args)

        self.workflow_input.update({'node_uuids': ['node_id'],
                                    'kernel_name': 'test_kernel',
                                    'ramdisk_name': 'test_ramdisk',
                                   'instance_boot_option': 'netboot',
                                    'root_device': 'smallest',
                                    'root_device_minimum_size': 2,
                                    'overwrite_root_device_hints': True})
        self.workflow.executions.create.assert_called_once_with(
            'tripleo.baremetal.v1.configure',
            workflow_input=self.workflow_input
        )


class TestDiscoverNode(fakes.TestOvercloudNode):

    def setUp(self):
        super(TestDiscoverNode, self).setUp()

        self.workflow = self.app.client_manager.workflow_engine
        execution = mock.Mock()
        execution.id = "IDID"
        self.workflow.executions.create.return_value = execution
        client = self.app.client_manager.tripleoclient
        self.websocket = client.messaging_websocket()

        self.cmd = overcloud_node.DiscoverNode(self.app, None)

        self.websocket.wait_for_messages.return_value = [{
            "status": "SUCCESS",
            "message": "Success",
            "registered_nodes": [{
                "uuid": "MOCK_NODE_UUID"
            }],
            "execution_id": "IDID"
        }]

        self.http_boot = '/var/lib/ironic/httpboot'

    def test_with_ip_range(self):
        argslist = ['--range', '10.0.0.0/24',
                    '--credentials', 'admin:password']
        verifylist = [('ip_addresses', '10.0.0.0/24'),
                      ('credentials', ['admin:password'])]

        parsed_args = self.check_parser(self.cmd, argslist, verifylist)
        self.cmd.take_action(parsed_args)

        self.workflow.executions.create.assert_called_once_with(
            'tripleo.baremetal.v1.discover_and_enroll_nodes',
            workflow_input={
                'ip_addresses': '10.0.0.0/24',
                'credentials': [['admin', 'password']],
                'kernel_name': 'file://%s/agent.kernel' % self.http_boot,
                'ramdisk_name': 'file://%s/agent.ramdisk' % self.http_boot,
                'instance_boot_option': 'local'
            }
        )

    def test_with_address_list(self):
        argslist = ['--ip', '10.0.0.1', '--ip', '10.0.0.2',
                    '--credentials', 'admin:password']
        verifylist = [('ip_addresses', ['10.0.0.1', '10.0.0.2']),
                      ('credentials', ['admin:password'])]

        parsed_args = self.check_parser(self.cmd, argslist, verifylist)
        self.cmd.take_action(parsed_args)

        self.workflow.executions.create.assert_called_once_with(
            'tripleo.baremetal.v1.discover_and_enroll_nodes',
            workflow_input={
                'ip_addresses': ['10.0.0.1', '10.0.0.2'],
                'credentials': [['admin', 'password']],
                'kernel_name': 'file://%s/agent.kernel' % self.http_boot,
                'ramdisk_name': 'file://%s/agent.ramdisk' % self.http_boot,
                'instance_boot_option': 'local'
            }
        )

    def test_with_all_options(self):
        argslist = ['--range', '10.0.0.0/24',
                    '--credentials', 'admin:password',
                    '--credentials', 'admin2:password2',
                    '--port', '623', '--port', '6230',
                    '--introspect', '--provide', '--run-validations',
                    '--no-deploy-image', '--instance-boot-option', 'netboot',
                    '--concurrency', '10']
        verifylist = [('ip_addresses', '10.0.0.0/24'),
                      ('credentials', ['admin:password', 'admin2:password2']),
                      ('port', [623, 6230]),
                      ('introspect', True),
                      ('run_validations', True),
                      ('concurrency', 10),
                      ('provide', True),
                      ('no_deploy_image', True),
                      ('instance_boot_option', 'netboot')]

        parsed_args = self.check_parser(self.cmd, argslist, verifylist)
        self.cmd.take_action(parsed_args)

        workflows_calls = [
            mock.call('tripleo.baremetal.v1.discover_and_enroll_nodes',
                      workflow_input={'ip_addresses': '10.0.0.0/24',
                                      'credentials': [['admin', 'password'],
                                                      ['admin2', 'password2']],
                                      'ports': [623, 6230],
                                      'kernel_name': None,
                                      'ramdisk_name': None,
                                      'instance_boot_option': 'netboot'}),
            mock.call('tripleo.baremetal.v1.introspect',
                      workflow_input={'node_uuids': ['MOCK_NODE_UUID'],
                                      'run_validations': True,
                                      'concurrency': 10}),
            mock.call('tripleo.baremetal.v1.provide',
                      workflow_input={'node_uuids': ['MOCK_NODE_UUID']}
                      )
        ]
        self.workflow.executions.create.assert_has_calls(workflows_calls)


class TestProvisionNode(fakes.TestOvercloudNode):

    def setUp(self):
        super(TestProvisionNode, self).setUp()

        self.workflow = self.app.client_manager.workflow_engine
        execution = mock.Mock()
        execution.id = "IDID"
        self.workflow.executions.create.return_value = execution
        client = self.app.client_manager.tripleoclient
        self.websocket = client.messaging_websocket()
        self.websocket.wait_for_messages.return_value = [{
            "status": "SUCCESS",
            "message": "Success",
            "environment": {"cat": "meow"},
            "execution": {"id": "IDID"}
        }]

        self.cmd = overcloud_node.ProvisionNode(self.app, None)

    def test_ok(self):
        with tempfile.NamedTemporaryFile() as inp:
            with tempfile.NamedTemporaryFile() as outp:
                with tempfile.NamedTemporaryFile() as keyf:
                    inp.write(b'- name: Compute\n- name: Controller\n')
                    inp.flush()
                    keyf.write(b'I am a key')
                    keyf.flush()
                    with open('{}.pub'.format(keyf.name), 'w') as f:
                        f.write('I am a key')

                    argslist = ['--output', outp.name,
                                '--overcloud-ssh-key', keyf.name,
                                inp.name]
                    verifylist = [('input', inp.name),
                                  ('output', outp.name),
                                  ('overcloud_ssh_key', keyf.name)]

                    parsed_args = self.check_parser(self.cmd,
                                                    argslist, verifylist)
                    self.cmd.take_action(parsed_args)

                    data = yaml.safe_load(outp)
                    self.assertEqual({"cat": "meow"}, data)

        self.workflow.executions.create.assert_called_once_with(
            'tripleo.baremetal_deploy.v1.deploy_roles',
            workflow_input={'roles': [{'name': 'Compute'},
                                      {'name': 'Controller'}],
                            'plan': 'overcloud',
                            'ssh_keys': ['I am a key'],
                            'ssh_user_name': 'heat-admin',
                            'concurrency': 20,
                            'timeout': 3600}
        )


class TestUnprovisionNode(fakes.TestOvercloudNode):

    def setUp(self):
        super(TestUnprovisionNode, self).setUp()

        self.workflow = self.app.client_manager.workflow_engine
        execution = mock.Mock()
        execution.id = "IDID"
        self.workflow.executions.create.return_value = execution
        client = self.app.client_manager.tripleoclient
        self.websocket = client.messaging_websocket()
        self.websocket.wait_for_messages.return_value = [{
            "status": "SUCCESS",
            "message": "Success",
            "environment": {"cat": "meow"},
            "execution": {"id": "IDID"}
        }]

        self.cmd = overcloud_node.UnprovisionNode(self.app, None)

    def test_ok(self):
        rv = mock.Mock()
        rv.output = json.dumps({
            'result': {
                'instances': [
                    {'hostname': 'compute-0', 'name': 'baremetal-1'},
                    {'hostname': 'controller-0', 'name': 'baremetal-2'}
                ]
            }
        })

        self.workflow.action_executions.create.return_value = rv
        with tempfile.NamedTemporaryFile() as inp:
            inp.write(b'- name: Compute\n- name: Controller\n')
            inp.flush()
            argslist = ['--yes', inp.name]
            verifylist = [('input', inp.name), ('yes', True)]

            parsed_args = self.check_parser(self.cmd,
                                            argslist, verifylist)
            self.cmd.take_action(parsed_args)

        self.workflow.executions.create.assert_called_once_with(
            'tripleo.baremetal_deploy.v1.undeploy_roles',
            workflow_input={
                'plan': 'overcloud',
                'roles': [{
                    'name': 'Unprovisioned',
                    'count': 0,
                    'instances': [
                        {'hostname': u'compute-0', 'provisioned': False},
                        {'hostname': u'controller-0', 'provisioned': False}
                    ]
                }]
            }
        )

    def test_ok_all(self):
        rv = mock.Mock()
        rv.output = json.dumps({
            'result': {
                'instances': [
                    {'hostname': 'compute-0', 'name': 'baremetal-1'},
                    {'hostname': 'controller-0', 'name': 'baremetal-2'}
                ]
            }
        })

        rv_provisioned = mock.Mock()
        rv_provisioned.output = json.dumps({
            'result': {
                'instances': [
                    {'hostname': 'compute-1', 'name': 'baremetal-3'},
                    {'hostname': 'controller-1', 'name': 'baremetal-4'}
                ]
            }
        })

        self.workflow.action_executions.create.side_effect = [
            rv, rv_provisioned
        ]
        with tempfile.NamedTemporaryFile() as inp:
            inp.write(b'- name: Compute\n- name: Controller\n')
            inp.flush()
            argslist = ['--all', '--yes', inp.name]
            verifylist = [('input', inp.name), ('yes', True), ('all', True)]

            parsed_args = self.check_parser(self.cmd,
                                            argslist, verifylist)
            self.cmd.take_action(parsed_args)

        self.workflow.executions.create.assert_called_once_with(
            'tripleo.baremetal_deploy.v1.undeploy_roles',
            workflow_input={
                'plan': 'overcloud',
                'roles': [{
                    'name': 'Unprovisioned',
                    'count': 0,
                    'instances': [
                        {'hostname': u'compute-0', 'provisioned': False},
                        {'hostname': u'controller-0', 'provisioned': False},
                        {'hostname': u'compute-1', 'provisioned': False},
                        {'hostname': u'controller-1', 'provisioned': False}
                    ]
                }]
            }
        )
