from signal_bot.main import run_cli, CLI_FAKE_SENDER
from signal_bot.config import Config


def make_config(tmp_path):
    return Config(
        phone_number="+440001111111",
        cli_path="signal-cli",
        log_dir=str(tmp_path),
        allowed_senders=None,
        data_dir=str(tmp_path),
    )


def test_cli_routes_command(tmp_path, monkeypatch):
    inputs = iter(["/test hello", ""])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    output = []
    monkeypatch.setattr("builtins.print", lambda *a, **kw: output.append(" ".join(str(x) for x in a)))
    run_cli(make_config(tmp_path))
    assert any("olleh" in line for line in output)


def test_cli_prints_banner(tmp_path, monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: (_ for _ in ()).throw(EOFError))
    output = []
    monkeypatch.setattr("builtins.print", lambda *a, **kw: output.append(" ".join(str(x) for x in a)))
    run_cli(make_config(tmp_path))
    assert any("Signaalbot CLI" in line for line in output)
    assert any(CLI_FAKE_SENDER in line for line in output)


def test_cli_no_response_for_plain_message(tmp_path, monkeypatch):
    inputs = iter(["just chatting", ""])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    output = []
    monkeypatch.setattr("builtins.print", lambda *a, **kw: output.append(" ".join(str(x) for x in a)))
    run_cli(make_config(tmp_path))
    assert not any("[bot]" in line for line in output)


def test_cli_logs_incoming_message(tmp_path, monkeypatch):
    inputs = iter(["/test hi", ""])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    monkeypatch.setattr("builtins.print", lambda *a, **kw: None)
    run_cli(make_config(tmp_path))
    log_files = list(tmp_path.glob("*.txt"))
    assert len(log_files) >= 1
    content = log_files[0].read_text()
    assert "[incoming]" in content


def test_cli_logs_outgoing_response(tmp_path, monkeypatch):
    inputs = iter(["/test hi", ""])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    monkeypatch.setattr("builtins.print", lambda *a, **kw: None)
    run_cli(make_config(tmp_path))
    log_files = list(tmp_path.glob("*.txt"))
    content = "".join(f.read_text() for f in log_files)
    assert "[outgoing]" in content


def test_cli_exits_on_empty_input(tmp_path, monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "")
    output = []
    monkeypatch.setattr("builtins.print", lambda *a, **kw: output.append(" ".join(str(x) for x in a)))
    run_cli(make_config(tmp_path))
    assert any("Bye" in line for line in output)


def test_cli_exits_on_eof(tmp_path, monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: (_ for _ in ()).throw(EOFError))
    output = []
    monkeypatch.setattr("builtins.print", lambda *a, **kw: output.append(" ".join(str(x) for x in a)))
    run_cli(make_config(tmp_path))
    assert any("Bye" in line for line in output)


def test_cli_unauthorized_sender_dropped(tmp_path, monkeypatch):
    config = Config(
        phone_number="+440001111111",
        cli_path="signal-cli",
        log_dir=str(tmp_path),
        allowed_senders=["+449999999999"],
        data_dir=str(tmp_path),
    )
    inputs = iter(["/test hello", ""])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    output = []
    monkeypatch.setattr("builtins.print", lambda *a, **kw: output.append(" ".join(str(x) for x in a)))
    run_cli(config)
    assert not any("[bot]" in line for line in output)
    assert any("unauthorized" in line for line in output)
