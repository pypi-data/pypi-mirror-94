#   Copyright 2018 Red Hat, Inc.
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

import mock

from osc_lib import exceptions as oscexc
from osc_lib.tests.utils import ParserException
from tripleoclient import constants
from tripleoclient import exceptions
from tripleoclient.tests.v1.overcloud_upgrade import fakes
from tripleoclient.v1 import overcloud_upgrade


class TestOvercloudUpgradePrepare(fakes.TestOvercloudUpgradePrepare):

    def setUp(self):
        super(TestOvercloudUpgradePrepare, self).setUp()

        # Get the command object to test
        app_args = mock.Mock()
        app_args.verbose_level = 1
        self.cmd = overcloud_upgrade.UpgradePrepare(self.app, app_args)

        uuid4_patcher = mock.patch('uuid.uuid4', return_value="UUID4")
        self.mock_uuid4 = uuid4_patcher.start()
        self.addCleanup(self.mock_uuid4.stop)

    @mock.patch('tripleoclient.utils.prompt_user_for_confirmation',
                return_value=True)
    @mock.patch('tripleoclient.v1.overcloud_deploy.DeployOvercloud.'
                'take_action')
    @mock.patch('tripleoclient.workflows.deployment.'
                'get_hosts_and_enable_ssh_admin', autospec=True)
    @mock.patch('tripleoclient.workflows.package_update.get_config',
                autospec=True)
    @mock.patch('tripleoclient.utils.prepend_environment', autospec=True)
    @mock.patch('tripleoclient.utils.get_stack',
                autospec=True)
    @mock.patch('tripleoclient.v1.overcloud_upgrade.UpgradePrepare.log',
                autospec=True)
    @mock.patch('yaml.safe_load')
    def test_upgrade_out(self,
                         mock_yaml,
                         mock_logger,
                         mock_get_stack,
                         add_env,
                         mock_get_config,
                         mock_enable_ssh_admin,
                         mock_overcloud_deploy,
                         mock_confirm):

        mock_stack = mock.Mock(parameters={'DeployIdentifier': ''})
        mock_stack.stack_name = 'overcloud'
        mock_get_stack.return_value = mock_stack
        mock_yaml.return_value = {'fake_container': 'fake_value'}
        add_env = mock.Mock()
        add_env.return_value = True
        argslist = ['--stack', 'overcloud', '--templates',
                    '--overcloud-ssh-enable-timeout', '10',
                    '--overcloud-ssh-port-timeout', '10']
        verifylist = [
            ('stack', 'overcloud'),
            ('templates', constants.TRIPLEO_HEAT_TEMPLATES),
            ('overcloud_ssh_enable_timeout', 10),
            ('overcloud_ssh_port_timeout', 10),
        ]

        parsed_args = self.check_parser(self.cmd, argslist, verifylist)
        with mock.patch('six.moves.builtins.open'):
            self.cmd.take_action(parsed_args)

        mock_overcloud_deploy.assert_called_once_with(parsed_args)
        args, kwargs = mock_overcloud_deploy.call_args
        # Check config_download arg is set to False
        self.assertEqual(args[0].config_download, False)
        mock_get_config.assert_called_once_with(mock.ANY,
                                                container=mock_stack.stack_name
                                                )
        mock_enable_ssh_admin.assert_called_once_with(
            self.cmd.log, self.app.client_manager, mock_stack,
            parsed_args.overcloud_ssh_network,
            parsed_args.overcloud_ssh_user, mock.ANY,
            10, 10)

    @mock.patch('tripleoclient.utils.prompt_user_for_confirmation',
                return_value=True)
    @mock.patch('tripleoclient.v1.overcloud_deploy.DeployOvercloud.'
                'take_action')
    @mock.patch('tripleoclient.utils.get_stack',
                autospec=True)
    @mock.patch('tripleoclient.utils.prepend_environment', autospec=True)
    @mock.patch('yaml.safe_load')
    def test_upgrade_failed(self, mock_yaml,
                            add_env, mock_get_stack, mock_overcloud_deploy,
                            mock_confirm):
        mock_overcloud_deploy.side_effect = exceptions.DeploymentError()
        mock_yaml.return_value = {'fake_container': 'fake_value'}
        mock_stack = mock.Mock(parameters={'DeployIdentifier': ''})
        mock_stack.stack_name = 'overcloud'
        mock_get_stack.return_value = mock_stack
        add_env = mock.Mock()
        add_env.return_value = True
        argslist = ['--stack', 'overcloud', '--templates', ]
        verifylist = [
            ('stack', 'overcloud'),
            ('templates', constants.TRIPLEO_HEAT_TEMPLATES),
        ]
        parsed_args = self.check_parser(self.cmd, argslist, verifylist)

        with mock.patch('six.moves.builtins.open'):
            self.assertRaises(exceptions.DeploymentError,
                              self.cmd.take_action, parsed_args)
        mock_overcloud_deploy.assert_called_once_with(parsed_args)

    @mock.patch('tripleo_common.update.check_neutron_mechanism_drivers')
    def test_upgrade_failed_wrong_driver(self, check_mech):
        check_mech.return_value = 'Wrong mech'
        mock_stack = mock.Mock(parameters={'DeployIdentifier': ''})
        argslist = (mock_stack, 'mock_stack', '/tmp', {},
                    {}, 1, '/tmp', {}, True, False, False, None)
        self.cmd.object_client = mock.Mock()
        self.assertRaises(oscexc.CommandError,
                          self.cmd._heat_deploy, *argslist)


class TestOvercloudUpgradeRun(fakes.TestOvercloudUpgradeRun):

    def setUp(self):
        super(TestOvercloudUpgradeRun, self).setUp()

        # Get the command object to test
        app_args = mock.Mock()
        app_args.verbose_level = 1
        self.cmd = overcloud_upgrade.UpgradeRun(self.app, app_args)

        uuid4_patcher = mock.patch('uuid.uuid4', return_value="UUID4")
        self.mock_uuid4 = uuid4_patcher.start()
        self.addCleanup(self.mock_uuid4.stop)

    @mock.patch('tripleoclient.utils.prompt_user_for_confirmation',
                return_value=True)
    @mock.patch('tripleoclient.workflows.package_update.update_ansible',
                autospec=True)
    @mock.patch('os.path.expanduser')
    @mock.patch('oslo_concurrency.processutils.execute')
    def test_upgrade_limit_with_playbook_and_user(
            self, mock_execute, mock_expanduser, upgrade_ansible,
            mock_confirm):
        mock_expanduser.return_value = '/home/fake/'
        argslist = ['--limit', 'Compute, Controller',
                    '--playbook', 'fake-playbook.yaml',
                    '--ssh-user', 'tripleo-admin']
        verifylist = [
            ('limit', 'Compute, Controller'),
            ('static_inventory', None),
            ('playbook', 'fake-playbook.yaml')
        ]

        parsed_args = self.check_parser(self.cmd, argslist, verifylist)

        with mock.patch('os.path.exists') as mock_exists, \
                mock.patch('six.moves.builtins.open') as mock_open:
            mock_exists.return_value = True
            self.cmd.take_action(parsed_args)
            upgrade_ansible.assert_called_once_with(
                self.app.client_manager,
                container='overcloud',
                nodes='Compute:Controller',
                inventory_file=mock_open().__enter__().read(),
                playbook='fake-playbook.yaml',
                node_user='tripleo-admin',
                tags='',
                skip_tags='',
                verbosity=1,
                extra_vars=None
            )

    @mock.patch('tripleoclient.utils.prompt_user_for_confirmation',
                return_value=True)
    @mock.patch('tripleoclient.workflows.package_update.update_ansible',
                autospec=True)
    @mock.patch('os.path.expanduser')
    @mock.patch('oslo_concurrency.processutils.execute')
    def test_upgrade_limit_all_playbooks_skip_validation(
            self, mock_execute, mock_expanduser, upgrade_ansible,
            mock_confirm):
        mock_expanduser.return_value = '/home/fake/'
        argslist = ['--limit', 'Compute', '--playbook', 'all',
                    '--skip-tags', 'validation']
        verifylist = [
            ('limit', 'Compute'),
            ('static_inventory', None),
            ('playbook', 'all'),
            ('skip_tags', 'validation')
        ]

        parsed_args = self.check_parser(self.cmd, argslist, verifylist)
        with mock.patch('os.path.exists') as mock_exists, \
                mock.patch('six.moves.builtins.open') as mock_open:
            mock_exists.return_value = True
            self.cmd.take_action(parsed_args)
            for book in constants.MAJOR_UPGRADE_PLAYBOOKS:
                upgrade_ansible.assert_any_call(
                    self.app.client_manager,
                    container='overcloud',
                    nodes='Compute',
                    inventory_file=mock_open().__enter__().read(),
                    playbook=book,
                    node_user='tripleo-admin',
                    tags='',
                    skip_tags='validation',
                    verbosity=1,
                    extra_vars=None
                )

    @mock.patch('tripleoclient.utils.prompt_user_for_confirmation',
                return_value=True)
    @mock.patch('tripleoclient.workflows.package_update.update_ansible',
                autospec=True)
    @mock.patch('os.path.expanduser')
    @mock.patch('oslo_concurrency.processutils.execute')
    def test_upgrade_limit_all_playbooks_only_validation(
            self, mock_execute, mock_expanduser, upgrade_ansible,
            mock_confirm):
        mock_expanduser.return_value = '/home/fake/'
        argslist = ['--limit', 'Compute', '--playbook', 'all',
                    '--tags', 'validation']
        verifylist = [
            ('limit', 'Compute'),
            ('static_inventory', None),
            ('playbook', 'all'),
            ('tags', 'validation')
        ]

        parsed_args = self.check_parser(self.cmd, argslist, verifylist)
        with mock.patch('os.path.exists') as mock_exists, \
                mock.patch('six.moves.builtins.open') as mock_open:
            mock_exists.return_value = True
            self.cmd.take_action(parsed_args)
            for book in constants.MAJOR_UPGRADE_PLAYBOOKS:
                upgrade_ansible.assert_any_call(
                    self.app.client_manager,
                    container='overcloud',
                    nodes='Compute',
                    inventory_file=mock_open().__enter__().read(),
                    playbook=book,
                    node_user='tripleo-admin',
                    tags='validation',
                    skip_tags='',
                    verbosity=1,
                    extra_vars=None
                )

    @mock.patch('tripleoclient.utils.prompt_user_for_confirmation',
                return_value=True)
    @mock.patch('tripleoclient.workflows.package_update.update_ansible',
                autospec=True)
    @mock.patch('os.path.expanduser')
    @mock.patch('oslo_concurrency.processutils.execute')
    def test_upgrade_nodes_with_playbook_no_skip_tags(
            self, mock_execute, mock_expanduser, upgrade_ansible,
            mock_confirm):
        mock_expanduser.return_value = '/home/fake/'
        argslist = ['--limit', 'compute-0,compute-1',
                    '--playbook', 'fake-playbook.yaml', ]
        verifylist = [
            ('limit', 'compute-0,compute-1'),
            ('static_inventory', None),
            ('playbook', 'fake-playbook.yaml'),
        ]

        parsed_args = self.check_parser(self.cmd, argslist, verifylist)
        with mock.patch('os.path.exists') as mock_exists, \
                mock.patch('six.moves.builtins.open') as mock_open:
            mock_exists.return_value = True
            self.cmd.take_action(parsed_args)
            upgrade_ansible.assert_called_once_with(
                self.app.client_manager,
                container='overcloud',
                nodes='compute-0:compute-1',
                inventory_file=mock_open().__enter__().read(),
                playbook='fake-playbook.yaml',
                node_user='tripleo-admin',
                tags='',
                skip_tags='',
                verbosity=1,
                extra_vars=None
            )

    @mock.patch('tripleoclient.utils.prompt_user_for_confirmation',
                return_value=True)
    @mock.patch('tripleoclient.workflows.package_update.update_ansible',
                autospec=True)
    @mock.patch('os.path.expanduser')
    @mock.patch('oslo_concurrency.processutils.execute')
    def test_upgrade_node_all_playbooks_skip_tags_default(
            self, mock_execute, mock_expanduser, upgrade_ansible,
            mock_confirm):
        mock_expanduser.return_value = '/home/fake/'
        argslist = ['--limit', 'swift-1', '--playbook', 'all']
        verifylist = [
            ('limit', 'swift-1'),
            ('static_inventory', None),
            ('playbook', 'all'),
        ]

        parsed_args = self.check_parser(self.cmd, argslist, verifylist)
        with mock.patch('os.path.exists') as mock_exists, \
                mock.patch('six.moves.builtins.open') as mock_open:
            mock_exists.return_value = True
            self.cmd.take_action(parsed_args)
            for book in constants.MAJOR_UPGRADE_PLAYBOOKS:
                upgrade_ansible.assert_any_call(
                    self.app.client_manager,
                    container='overcloud',
                    nodes='swift-1',
                    inventory_file=mock_open().__enter__().read(),
                    playbook=book,
                    node_user='tripleo-admin',
                    tags='',
                    skip_tags='',
                    verbosity=1,
                    extra_vars=None
                )

    @mock.patch('tripleoclient.utils.prompt_user_for_confirmation',
                return_value=True)
    @mock.patch('tripleoclient.workflows.package_update.update_ansible',
                autospec=True)
    @mock.patch('os.path.expanduser')
    @mock.patch('oslo_concurrency.processutils.execute')
    def test_upgrade_node_all_playbooks_skip_tags_all_supported(
            self, mock_execute, mock_expanduser, upgrade_ansible,
            mock_confirm):
        mock_expanduser.return_value = '/home/fake/'
        argslist = ['--limit', 'swift-1', '--playbook', 'all',
                    '--skip-tags', 'pre-upgrade,validation']
        verifylist = [
            ('limit', 'swift-1'),
            ('static_inventory', None),
            ('playbook', 'all'),
            ('skip_tags', 'pre-upgrade,validation')
        ]

        parsed_args = self.check_parser(self.cmd, argslist, verifylist)
        with mock.patch('os.path.exists') as mock_exists, \
                mock.patch('six.moves.builtins.open') as mock_open:
            mock_exists.return_value = True
            self.cmd.take_action(parsed_args)
            for book in constants.MAJOR_UPGRADE_PLAYBOOKS:
                upgrade_ansible.assert_any_call(
                    self.app.client_manager,
                    container='overcloud',
                    nodes='swift-1',
                    inventory_file=mock_open().__enter__().read(),
                    playbook=book,
                    node_user='tripleo-admin',
                    tags='',
                    skip_tags='pre-upgrade,validation',
                    verbosity=1,
                    extra_vars=None
                )

    @mock.patch('tripleoclient.workflows.package_update.update_ansible',
                autospec=True)
    @mock.patch('os.path.expanduser')
    @mock.patch('oslo_concurrency.processutils.execute')
    def test_upgrade_with_no_limit(
            self, mock_execute, mock_expanduser, upgrade_ansible):
        mock_expanduser.return_value = '/home/fake/'
        argslist = []
        verifylist = []
        self.assertRaises(ParserException, lambda: self.check_parser(
            self.cmd, argslist, verifylist))

    @mock.patch('tripleoclient.utils.prompt_user_for_confirmation',
                return_value=True)
    @mock.patch('tripleoclient.workflows.package_update.update_ansible',
                autospec=True)
    @mock.patch('os.path.expanduser')
    @mock.patch('oslo_concurrency.processutils.execute')
    # it is 'validation' not 'validations'
    def test_upgrade_skip_tags_validations(self, mock_execute,
                                           mock_expanduser, upgrade_ansible,
                                           mock_confirm):
        mock_expanduser.return_value = '/home/fake/'
        argslist = ['--limit', 'overcloud-compute-1',
                    '--skip-tags', 'validations']
        verifylist = [
            ('limit', 'overcloud-compute-1'),
            ('static_inventory', None),
            ('playbook', 'all'),
            ('skip_tags', 'validations'),
        ]
        parsed_args = self.check_parser(self.cmd, argslist, verifylist)
        with mock.patch('os.path.exists') as mock_exists, \
                mock.patch('six.moves.builtins.open'):
            mock_exists.return_value = True
            self.assertRaises(exceptions.InvalidConfiguration,
                              lambda: self.cmd.take_action(parsed_args))

    @mock.patch('tripleoclient.utils.prompt_user_for_confirmation',
                return_value=True)
    @mock.patch('tripleoclient.workflows.package_update.update_ansible',
                autospec=True)
    @mock.patch('os.path.expanduser')
    @mock.patch('oslo_concurrency.processutils.execute')
    # should only support the constants.MAJOR_UPGRADE_SKIP_TAGS
    def test_upgrade_skip_tags_unsupported_validation_anything_else(
            self, mock_execute, mock_expanduser, upgrade_ansible,
            mock_confirm):
        mock_expanduser.return_value = '/home/fake/'
        argslist = ['--limit', 'overcloud-compute-1',
                    '--skip-tags', 'validation,anything-else']
        verifylist = [
            ('limit', 'overcloud-compute-1'),
            ('static_inventory', None),
            ('playbook', 'all'),
            ('skip_tags', 'validation,anything-else'),
        ]
        parsed_args = self.check_parser(self.cmd, argslist, verifylist)
        with mock.patch('os.path.exists') as mock_exists, \
                mock.patch('six.moves.builtins.open'):
            mock_exists.return_value = True
            self.assertRaises(exceptions.InvalidConfiguration,
                              lambda: self.cmd.take_action(parsed_args))

    @mock.patch('tripleoclient.utils.prompt_user_for_confirmation',
                return_value=True)
    @mock.patch('tripleoclient.workflows.package_update.update_ansible',
                autospec=True)
    @mock.patch('os.path.expanduser')
    @mock.patch('oslo_concurrency.processutils.execute')
    # should only support the constants.MAJOR_UPGRADE_SKIP_TAGS
    def test_upgrade_skip_tags_unsupported_pre_upgrade_anything_else(
            self, mock_execute, mock_expanduser, upgrade_ansible,
            mock_confirm):
        mock_expanduser.return_value = '/home/fake/'
        argslist = ['--limit', 'overcloud-compute-1',
                    '--skip-tags', 'pre-upgrade,anything-else']
        verifylist = [
            ('limit', 'overcloud-compute-1'),
            ('static_inventory', None),
            ('playbook', 'all'),
            ('skip_tags', 'pre-upgrade,anything-else'),
        ]
        parsed_args = self.check_parser(self.cmd, argslist, verifylist)
        with mock.patch('os.path.exists') as mock_exists, \
                mock.patch('six.moves.builtins.open'):
            mock_exists.return_value = True
            self.assertRaises(exceptions.InvalidConfiguration,
                              lambda: self.cmd.take_action(parsed_args))
