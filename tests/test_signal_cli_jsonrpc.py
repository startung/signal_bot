import json
from io import BytesIO
from unittest.mock import patch, MagicMock
from signal_bot.signal_cli_jsonrpc import SignalCliJsonRpc
from signal_bot.message import Direction


ACCOUNT = "+447786000000"


def make_envelope(source, timestamp_ms, message):
    return {
        "envelope": {
            "source": source,
            "sourceNumber": source,
            "timestamp": timestamp_ms,
            "dataMessage": {
                "timestamp": timestamp_ms,
                "message": message,
            },
        }
    }


def mock_socket(response: dict):
    payload = (json.dumps(response) + "\n").encode()
    sock = MagicMock()
    sock.__enter__ = lambda s: s
    sock.__exit__ = MagicMock(return_value=False)
    sock.recv.side_effect = [payload, b""]
    return sock


def test_send_calls_jsonrpc(monkeypatch):
    cli = SignalCliJsonRpc(account=ACCOUNT, host="localhost", port=7583)
    sock = mock_socket({"jsonrpc": "2.0", "result": None, "id": 1})
    with patch("signal_bot.signal_cli_jsonrpc.socket.create_connection", return_value=sock):
        cli.send("+449999999999", "Hello!")
    sent = sock.sendall.call_args[0][0].decode()
    data = json.loads(sent.strip())
    assert data["method"] == "send"
    assert data["params"]["recipient"] == ["+449999999999"]
    assert data["params"]["message"] == "Hello!"
    assert data["params"]["account"] == ACCOUNT


def test_receive_parses_messages():
    cli = SignalCliJsonRpc(account=ACCOUNT)
    envelope = make_envelope("+449999999999", 1700000000000, "Hello bot!")
    sock = mock_socket({"jsonrpc": "2.0", "result": [envelope], "id": 2})
    with patch("signal_bot.signal_cli_jsonrpc.socket.create_connection", return_value=sock):
        messages = cli.receive()
    assert len(messages) == 1
    msg = messages[0]
    assert msg.sender == "+449999999999"
    assert msg.recipient == ACCOUNT
    assert msg.body == "Hello bot!"
    assert msg.direction == Direction.INCOMING


def test_receive_multiple_messages():
    cli = SignalCliJsonRpc(account=ACCOUNT)
    envelopes = [
        make_envelope("+440001111111", 1700000000000, "First"),
        make_envelope("+440002222222", 1700000001000, "Second"),
    ]
    sock = mock_socket({"jsonrpc": "2.0", "result": envelopes, "id": 2})
    with patch("signal_bot.signal_cli_jsonrpc.socket.create_connection", return_value=sock):
        messages = cli.receive()
    assert len(messages) == 2
    assert messages[0].body == "First"
    assert messages[1].body == "Second"


def test_receive_empty_result():
    cli = SignalCliJsonRpc(account=ACCOUNT)
    sock = mock_socket({"jsonrpc": "2.0", "result": [], "id": 2})
    with patch("signal_bot.signal_cli_jsonrpc.socket.create_connection", return_value=sock):
        messages = cli.receive()
    assert messages == []


def test_receive_skips_non_data_envelopes():
    cli = SignalCliJsonRpc(account=ACCOUNT)
    receipt = {"envelope": {"source": "+449999999999", "timestamp": 1700000000000, "receiptMessage": {"type": "DELIVERY"}}}
    data = make_envelope("+449999999999", 1700000001000, "Real message")
    sock = mock_socket({"jsonrpc": "2.0", "result": [receipt, data], "id": 2})
    with patch("signal_bot.signal_cli_jsonrpc.socket.create_connection", return_value=sock):
        messages = cli.receive()
    assert len(messages) == 1
    assert messages[0].body == "Real message"


def test_receive_skips_null_message_body():
    cli = SignalCliJsonRpc(account=ACCOUNT)
    envelope = make_envelope("+449999999999", 1700000000000, None)
    sock = mock_socket({"jsonrpc": "2.0", "result": [envelope], "id": 2})
    with patch("signal_bot.signal_cli_jsonrpc.socket.create_connection", return_value=sock):
        messages = cli.receive()
    assert messages == []


def test_receive_sets_timestamp_from_envelope():
    cli = SignalCliJsonRpc(account=ACCOUNT)
    envelope = make_envelope("+449999999999", 1700000000000, "Timed")
    sock = mock_socket({"jsonrpc": "2.0", "result": [envelope], "id": 2})
    with patch("signal_bot.signal_cli_jsonrpc.socket.create_connection", return_value=sock):
        messages = cli.receive()
    assert messages[0].timestamp.year == 2023


def test_jsonrpc_error_raises():
    cli = SignalCliJsonRpc(account=ACCOUNT)
    sock = mock_socket({"jsonrpc": "2.0", "error": {"code": -1, "message": "bad"}, "id": 1})
    with patch("signal_bot.signal_cli_jsonrpc.socket.create_connection", return_value=sock):
        try:
            cli.send("+449999999999", "Hello!")
            assert False, "expected RuntimeError"
        except RuntimeError as e:
            assert "JSON-RPC error" in str(e)
