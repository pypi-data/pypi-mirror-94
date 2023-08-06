# -*- coding: utf-8 -*-

# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import json
import mock
import socket

from tripleoclient import plugin
from tripleoclient.tests import base
from tripleoclient.tests import fakes


class TestPlugin(base.TestCase):

    @mock.patch("websocket.create_connection")
    def test_make_client(self, ws_create_connection):
        clientmgr = mock.MagicMock()
        clientmgr.get_endpoint_for_service_type.return_value = fakes.WS_URL

        clientmgr.auth.get_token.return_value = "TOKEN"
        clientmgr.auth_ref.project_id = "ID"
        clientmgr.cacert = None
        ws_create_connection.return_value.recv.return_value = json.dumps({
            "headers": {
                "status": 200
            }
        })
        client = plugin.make_client(clientmgr)

        websocket = client.messaging_websocket()
        # The second access should not return the same client:
        self.assertIsNot(client.messaging_websocket(), websocket)

        plugin.make_client(clientmgr)

        # And the functions should only be called when the client is created:
        self.assertEqual(clientmgr.auth.get_token.call_count, 2)
        self.assertEqual(clientmgr.get_endpoint_for_service_type.call_count, 2)
        ws_create_connection.assert_called_with("ws://0.0.0.0")

    @mock.patch("websocket.create_connection")
    def test_invalid_json(self, ws_create_connection):
        clientmgr = mock.MagicMock()
        clientmgr.get_endpoint_for_service_type.return_value = fakes.WS_URL

        clientmgr.auth.get_token.return_value = "TOKEN"
        clientmgr.auth_ref.project_id = "ID"
        clientmgr.cacert = None
        ws_create_connection.return_value.recv.return_value = "BAD JSON"
        client = plugin.make_client(clientmgr)

        # NOTE(d0ugal): Manually catching errors rather than using assertRaises
        #               so we can assert the message.
        try:
            client.messaging_websocket()
            self.assertFail()
        except ValueError as e:
            self.assertEqual(
                str(e), "No JSON object could be decoded; 'BAD JSON'")

    @mock.patch.object(plugin.WebsocketClient, "recv")
    @mock.patch("websocket.create_connection")
    def test_handle_websocket_multiple(self, ws_create_connection, recv_mock):

        send_ack = {
            "headers": {
                "status": 200
            }
        }

        # Creating the websocket sends three messages and closing sends one.
        # The one being tested is wrapped between these
        recv_mock.side_effect = [send_ack, send_ack, send_ack, {
            "body": {
                "payload": {
                    "status": 200,
                    "message": "Result for IDID",
                    "execution_id": "IDID",
                }
            }
        }, send_ack]

        clientmgr = mock.MagicMock()
        clientmgr.get_endpoint_for_service_type.return_value = fakes.WS_URL
        clientmgr.auth.get_token.return_value = "TOKEN"
        clientmgr.auth_ref.project_id = "ID"
        clientmgr.cacert = None

        client = plugin.make_client(clientmgr)

        with client.messaging_websocket() as ws:
            for payload in ws.wait_for_messages():
                self.assertEqual(payload, {
                    "status": 200,
                    "message": "Result for IDID",
                    "execution_id": "IDID",
                })
                # We only want to test the first message, as there is only one.
                # The last one, the send_ack will be used by the context
                # manager when it is closed.
                break

    @mock.patch("websocket.create_connection")
    def test_websocket_creation_error(self, ws_create_connection):

        ws_create_connection.side_effect = socket.error

        clientmgr = mock.MagicMock()
        clientmgr.get_endpoint_for_service_type.return_value = fakes.WS_URL
        clientmgr.auth.get_token.return_value = "TOKEN"
        clientmgr.auth_ref.project_id = "ID"
        clientmgr.cacert = None

        client = plugin.make_client(clientmgr)

        msg = ("Could not establish a connection to the Zaqar websocket. The "
               "command was sent but the answer could not be read.")
        with mock.patch('tripleoclient.plugin.LOG') as mock_log:
            self.assertRaises(socket.error, client.messaging_websocket)
            mock_log.error.assert_called_once_with(msg)

    @mock.patch("websocket.create_connection")
    def test_make_tls_client(self, ws_create_connection):
        clientmgr = mock.MagicMock()
        clientmgr.get_endpoint_for_service_type.return_value = fakes.WSS_URL

        clientmgr.auth.get_token.return_value = "TOKEN"
        clientmgr.auth_ref.project_id = "ID"
        clientmgr.cacert = '/etc/pki/ca-trust/source/anchors/cm-local-ca.pem'
        ws_create_connection.return_value.recv.return_value = json.dumps({
            "headers": {
                "status": 200
            }
        })
        client = plugin.make_client(clientmgr)

        websocket = client.messaging_websocket()
        # The second access should not return the same client:
        self.assertIsNot(client.messaging_websocket(), websocket)

        plugin.make_client(clientmgr)

        # And the functions should only be called when the client is created:
        self.assertEqual(clientmgr.auth.get_token.call_count, 2)
        self.assertEqual(clientmgr.get_endpoint_for_service_type.call_count, 2)
        ws_create_connection.assert_called_with(
            "wss://0.0.0.0",
            sslopt={'ca_certs':
                    '/etc/pki/ca-trust/source/anchors/cm-local-ca.pem'})
