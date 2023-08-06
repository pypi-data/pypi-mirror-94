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

import json
import tempfile

from osc_lib.tests import utils as test_utils

from tripleoclient.tests.v1.baremetal import fakes
from tripleoclient.v1 import overcloud_bios


class Base(fakes.TestBaremetal):
    def setUp(self):
        super(Base, self).setUp()
        self.workflow = self.app.client_manager.workflow_engine
        self.conf = {
            "settings": [
                {"name": "virtualization", "value": "on"},
                {"name": "hyperthreading", "value": "on"}
            ]
        }
        tripleoclient = self.app.client_manager.tripleoclient
        self.websocket = tripleoclient.messaging_websocket()
        self.websocket.wait_for_messages.return_value = iter([{
            'status': "SUCCESS",
            'execution_id': 'fake id',
            'root_execution_id': 'fake id',
        }])

        self.execution = self.workflow.executions.create.return_value
        self.execution.id = 'fake id'
        self.execution.output = '{"result": null}'


class TestConfigureBIOS(Base):

    def setUp(self):
        super(TestConfigureBIOS, self).setUp()
        self.cmd = overcloud_bios.ConfigureBIOS(self.app, None)

    def test_configure_specified_nodes_ok(self):
        conf = json.dumps(self.conf)
        arglist = ['--configuration', conf, 'node_uuid1', 'node_uuid2']
        verifylist = [
            ('node_uuids', ['node_uuid1', 'node_uuid2']),
            ('configuration', conf)
        ]
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        self.cmd.take_action(parsed_args)

        self.workflow.executions.create.assert_called_once_with(
            'tripleo.baremetal.v1.apply_bios_settings',
            workflow_input={
                'node_uuids': ['node_uuid1', 'node_uuid2'],
                'configuration': self.conf,
            }
        )

    def test_configure_specified_nodes_and_configuration_from_file(self):
        with tempfile.NamedTemporaryFile('w+t') as fp:
            json.dump(self.conf, fp)
            fp.flush()
            arglist = ['--configuration', fp.name, 'node_uuid1', 'node_uuid2']
            verifylist = [
                ('node_uuids', ['node_uuid1', 'node_uuid2']),
                ('configuration', fp.name)
            ]
            parsed_args = self.check_parser(self.cmd, arglist, verifylist)

            self.cmd.take_action(parsed_args)

        self.workflow.executions.create.assert_called_once_with(
            'tripleo.baremetal.v1.apply_bios_settings',
            workflow_input={
                'node_uuids': ['node_uuid1', 'node_uuid2'],
                'configuration': self.conf,
            }
        )

    def test_configure_no_nodes(self):
        arglist = ['--configuration', '{}']
        verifylist = [
            ('configuration', '{}')
        ]
        self.assertRaises(test_utils.ParserException, self.check_parser,
                          self.cmd, arglist, verifylist)
        self.assertFalse(self.workflow.executions.create.called)

    def test_configure_specified_nodes_and_configuration_not_yaml(self):
        arglist = ['--configuration', ':', 'node_uuid1', 'node_uuid2']
        verifylist = [
            ('node_uuids', ['node_uuid1', 'node_uuid2']),
            ('configuration', ':')
        ]
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        self.assertRaisesRegex(RuntimeError, 'cannot be parsed as YAML',
                               self.cmd.take_action, parsed_args)
        self.assertFalse(self.workflow.executions.create.called)

    def test_configure_specified_nodes_and_configuration_bad_type(self):
        for conf in ('[]', '{"settings": 42}', '{settings: [42]}'):
            arglist = ['--configuration', conf, 'node_uuid1', 'node_uuid2']
            verifylist = [
                ('node_uuids', ['node_uuid1', 'node_uuid2']),
                ('configuration', conf)
            ]
            parsed_args = self.check_parser(self.cmd, arglist, verifylist)

            self.assertRaises(TypeError, self.cmd.take_action, parsed_args)
            self.assertFalse(self.workflow.executions.create.called)

    def test_configure_specified_nodes_and_configuration_bad_value(self):
        conf = '{"another_key": [{}]}'
        arglist = ['--configuration', conf, 'node_uuid1', 'node_uuid2']
        verifylist = [
            ('node_uuids', ['node_uuid1', 'node_uuid2']),
            ('configuration', conf)
        ]
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        self.assertRaises(ValueError, self.cmd.take_action, parsed_args)
        self.assertFalse(self.workflow.executions.create.called)

    def test_configure_uuids_and_all_both_specified(self):
        conf = json.dumps(self.conf)
        arglist = ['--configuration', conf, 'node_uuid1', 'node_uuid2',
                   '--all-manageable']
        verifylist = [
            ('node_uuids', ['node_uuid1', 'node_uuid2']),
            ('configuration', conf),
            ('all-manageable', True)
        ]
        self.assertRaises(test_utils.ParserException, self.check_parser,
                          self.cmd, arglist, verifylist)

    def test_configure_all_manageable_nodes_ok(self):
        conf = json.dumps(self.conf)
        arglist = ['--configuration', conf, '--all-manageable']
        verifylist = [
            ('all_manageable', True),
            ('configuration', conf)
        ]
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        self.cmd.take_action(parsed_args)

        self.workflow.executions.create.assert_called_once_with(
            'tripleo.baremetal.v1.apply_bios_settings_on_manageable_nodes',
            workflow_input={'configuration': self.conf})

    def test_configure_all_manageable_nodes_fail(self):
        conf = json.dumps(self.conf)
        arglist = ['--configuration', conf, '--all-manageable']
        verifylist = [
            ('all_manageable', True),
            ('configuration', conf)
        ]

        self.websocket.wait_for_messages.return_value = iter([{
            "status": "FAILED",
            "message": "Test failure.",
            'execution_id': 'fake id',
            'root_execution_id': 'fake id',
        }])
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        self.assertRaisesRegex(RuntimeError, 'Failed to apply BIOS settings',
                               self.cmd.take_action, parsed_args)

        self.workflow.executions.create.assert_called_once_with(
            'tripleo.baremetal.v1.apply_bios_settings_on_manageable_nodes',
            workflow_input={'configuration': self.conf})


class TestResetBIOS(Base):

    def setUp(self):
        super(TestResetBIOS, self).setUp()
        self.cmd = overcloud_bios.ResetBIOS(self.app, None)

    def test_reset_specified_nodes_ok(self):
        arglist = ['node_uuid1', 'node_uuid2']
        verifylist = [('node_uuids', ['node_uuid1', 'node_uuid2'])]
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        self.cmd.take_action(parsed_args)

        self.workflow.executions.create.assert_called_once_with(
            'tripleo.baremetal.v1.reset_bios_settings',
            workflow_input={'node_uuids': ['node_uuid1', 'node_uuid2']})

    def test_reset_specified_nodes_fail(self):
        arglist = ['node_uuid1', 'node_uuid2']
        verifylist = [('node_uuids', ['node_uuid1', 'node_uuid2'])]

        self.websocket.wait_for_messages.return_value = iter([{
            "status": "FAILED",
            "message": "Test failure.",
            'execution_id': 'fake id',
            'root_execution_id': 'fake id',
        }])
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        self.assertRaisesRegex(RuntimeError, 'Failed to reset BIOS settings',
                               self.cmd.take_action, parsed_args)

        self.workflow.executions.create.assert_called_once_with(
            'tripleo.baremetal.v1.reset_bios_settings',
            workflow_input={'node_uuids': ['node_uuid1', 'node_uuid2']})

    def test_reset_all_manageable_nodes_ok(self):
        arglist = ['--all-manageable']
        verifylist = [('all_manageable', True)]
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        self.cmd.take_action(parsed_args)

        self.workflow.executions.create.assert_called_once_with(
            'tripleo.baremetal.v1.reset_bios_settings_on_manageable_nodes',
            workflow_input={})

    def test_reset_all_manageable_nodes_fail(self):
        arglist = ['--all-manageable']
        verifylist = [('all_manageable', True)]

        self.websocket.wait_for_messages.return_value = iter([{
            "status": "FAILED",
            "message": "Test failure.",
            'execution_id': 'fake id',
            'root_execution_id': 'fake id',
        }])
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        self.assertRaisesRegex(RuntimeError, 'Failed to reset BIOS settings',
                               self.cmd.take_action, parsed_args)

        self.workflow.executions.create.assert_called_once_with(
            'tripleo.baremetal.v1.reset_bios_settings_on_manageable_nodes',
            workflow_input={})

    def test_reset_no_nodes(self):
        arglist = []
        verifylist = []
        self.assertRaises(test_utils.ParserException, self.check_parser,
                          self.cmd, arglist, verifylist)
        self.assertFalse(self.workflow.executions.create.called)

    def test_reset_uuids_and_all_both_specified(self):
        arglist = ['node_uuid1', 'node_uuid2', '--all-manageable']
        verifylist = [
            ('node_uuids', ['node_uuid1', 'node_uuid2']),
            ('all-manageable', True)
        ]
        self.assertRaises(test_utils.ParserException, self.check_parser,
                          self.cmd, arglist, verifylist)
