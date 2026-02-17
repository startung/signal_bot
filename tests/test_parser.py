from signal_bot.parser import parse_command


def test_detects_command():
    result = parse_command("/test hello, world!")
    assert result is not None


def test_extracts_command_name():
    result = parse_command("/test hello, world!")
    assert result.command == "test"


def test_extracts_arguments():
    result = parse_command("/test hello, world!")
    assert result.args == "hello, world!"


def test_not_a_command():
    result = parse_command("just a regular message")
    assert result is None


def test_slash_alone_is_not_a_command():
    result = parse_command("/")
    assert result is None


def test_command_with_no_args():
    result = parse_command("/test")
    assert result is not None
    assert result.command == "test"
    assert result.args == ""


def test_extra_whitespace_stripped_from_args():
    result = parse_command("/test   hello   ")
    assert result.command == "test"
    assert result.args == "hello"


def test_different_command_name():
    result = parse_command("/other some args")
    assert result.command == "other"
    assert result.args == "some args"
