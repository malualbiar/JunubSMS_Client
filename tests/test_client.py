#Tests for the JunubSMS Python client.

import pytest
from unittest.mock import MagicMock, patch

from junubsms import JunubSMSClient, JunubSMSError
from junubsms.models import SMSResult, DeliveryStatus, IncomingMessage, Contact

#  Fixtures and helpers

@pytest.fixture
def client():
    return JunubSMSClient(username="testuser", token="test-token")


def mock_response(payload: dict) -> MagicMock:
    """Return a mock requests.Response with a given JSON payload."""
    resp = MagicMock()
    resp.json.return_value = payload
    resp.raise_for_status.return_value = None
    return resp


#  Client tests

class TestClient:
    def test_creates_message_and_admin_resources(self, client):
        assert client.messages is not None
        assert client.admin is not None

    def test_context_manager_closes_session(self):
        with JunubSMSClient(username="u", token="t") as c:
            c._session.close = MagicMock()
        c._session.close.assert_called_once()

    def test_from_credentials_fetches_token(self):
        token_response = mock_response({"data": {"h": "abc123"}, "error_string": None})
        with patch("requests.get", return_value=token_response):
            c = JunubSMSClient.from_credentials("alice", "password")
        assert c._token == "abc123"

    def test_from_credentials_raises_on_error(self):
        error_response = mock_response({"error_string": "ERR 100"})
        with patch("requests.get", return_value=error_response):
            with pytest.raises(JunubSMSError) as exc_info:
                JunubSMSClient.from_credentials("alice", "wrong")
        assert exc_info.value.code == "ERR 100"


#  Messages 

class TestMessages:
    def test_send_returns_sms_results(self, client):
        payload = {
            "data": [{"status": "OK", "error": "0", "smslog_id": "42", "queue": "abc", "to": "0912345678"}],
            "error_string": None,
        }
        
        client._session.get = MagicMock(return_value=mock_response(payload))
        results = client.messages.send(to="0912345678", msg="Hello!")

        assert len(results) == 1
        assert isinstance(results[0], SMSResult)
        assert results[0].ok is True
        assert results[0].to == "0912345678"

    def test_send_raises_on_api_error(self, client):
        client._session.get = MagicMock(return_value=mock_response({"error_string": "ERR 201"}))
        with pytest.raises(JunubSMSError) as exc_info:
            client.messages.send(to="", msg="")
        assert exc_info.value.code == "ERR 201"

    def test_outgoing_returns_delivery_statuses(self, client):
        payload = {
            "data": [{"smslog_id": "1", "src": "Brand", "dst": "0912345678", "msg": "Hi", "dt": "2024-01-01 10:00:00", "status": "1", "queue": "q1"}],
            "error_string": None,
        }
        client._session.get = MagicMock(return_value=mock_response(payload))
        results = client.messages.outgoing()

        assert len(results) == 1
        assert isinstance(results[0], DeliveryStatus)

    def test_incoming_returns_messages(self, client):
        payload = {
            "data": [{"id": "5", "src": "+249123456789", "dst": "1234", "msg": "VOTE A", "dt": "2024-01-01 12:00:00", "status": "1", "kwd": "VOTE"}],
            "error_string": None,
        }
        client._session.get = MagicMock(return_value=mock_response(payload))
        results = client.messages.incoming()

        assert isinstance(results[0], IncomingMessage)
        assert results[0].kwd == "VOTE"

    def test_get_contacts_returns_contacts(self, client):
        payload = {
            "data": [{"pid": "1", "gpid": "2", "p_desc": "Alice", "p_num": "0912345678", "email": "a@b.com", "group_name": "Staff", "code": "STAFF"}],
            "error_string": None,
        }
        client._session.get = MagicMock(return_value=mock_response(payload))
        contacts = client.messages.get_contacts("Alice")

        assert isinstance(contacts[0], Contact)
        assert contacts[0].p_desc == "Alice"

    def test_credit_returns_credit_info(self, client):
        payload = {"data": {"balance": "500.00", "credit": "500"}, "error_string": None}
        client._session.get = MagicMock(return_value=mock_response(payload))
        info = client.messages.credit()

        assert info.balance == "500.00"


#  Admin tests

class TestAdmin:
    def test_add_account_calls_correct_op(self, client):
        client._session.get = MagicMock(return_value=mock_response({"error_string": None, "data": {}}))
        client.admin.add_account(username="bob", password="pass", name="Bob", email="bob@example.com")

        call_params = client._session.get.call_args[1]["params"]
        assert call_params["op"] == "accountadd"
        assert call_params["data_username"] == "bob"

    def test_view_credit_returns_balance(self, client):
        payload = {"data": {"balance": "250.00"}, "error_string": None}
        client._session.get = MagicMock(return_value=mock_response(payload))

        assert client.admin.view_credit("bob") == "250.00"

    def test_add_credit_passes_amount(self, client):
        client._session.get = MagicMock(return_value=mock_response({"error_string": None, "data": {}}))
        client.admin.add_credit("bob", 100)

        call_params = client._session.get.call_args[1]["params"]
        assert call_params["data_amount"] == 100

    def test_ban_and_unban_account(self, client):
        client._session.get = MagicMock(return_value=mock_response({"error_string": None}))
        client.admin.ban_account("bob")
        assert client._session.get.call_args[1]["params"]["op"] == "accountban"

        client.admin.unban_account("bob")
        assert client._session.get.call_args[1]["params"]["op"] == "accountunban"

#  Exceptions 

class TestExceptions:
    def test_error_message_from_known_code(self):
        err = JunubSMSError("ERR 100")
        assert "Authentication" in str(err)

    def test_error_message_from_unknown_code(self):
        err = JunubSMSError("ERR 999")
        assert "Unknown error" in str(err)

    def test_custom_message_overrides_lookup(self):
        err = JunubSMSError("ERR 100", "Custom message")
        assert "Custom message" in str(err)