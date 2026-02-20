import json
from pathlib import Path
from unittest.mock import patch, MagicMock
from signal_bot.app_interface import CommandApp
from signal_bot.apps.date_app import DateApp


def make_app(tmp_path=None):
    if tmp_path is not None:
        return DateApp(data_dir=tmp_path)
    return DateApp()


def test_is_a_command_app():
    app = make_app()
    assert isinstance(app, CommandApp)


def test_name_is_date():
    app = make_app()
    assert app.name == "date"


def test_no_args_no_default_returns_utc():
    app = make_app()
    response = app.handle("", sender="+440001111111")
    assert "UTC" in response


@patch.object(DateApp, "_lookup_timezone", return_value="Europe/London")
def test_city_returns_local_time(mock_tz):
    app = make_app()
    response = app.handle("London", sender="+440001111111")
    assert "London" in response


@patch.object(DateApp, "_lookup_timezone", return_value="America/New_York")
def test_city_and_country_returns_local_time(mock_tz):
    app = make_app()
    response = app.handle("New York, US", sender="+440001111111")
    assert "New York" in response


@patch.object(DateApp, "_lookup_timezone", return_value="Europe/London")
def test_set_default_city(mock_tz):
    app = make_app()
    response = app.handle("set London, GB", sender="+440001111111")
    assert "London" in response
    assert "default" in response.lower()


@patch.object(DateApp, "_lookup_timezone", return_value="Asia/Tokyo")
def test_date_uses_default_after_set(mock_tz):
    app = make_app()
    app.handle("set Tokyo, JP", sender="+440001111111")
    response = app.handle("", sender="+440001111111")
    assert "Tokyo" in response


@patch.object(DateApp, "_lookup_timezone", return_value="Asia/Tokyo")
def test_default_is_per_sender(mock_tz):
    app = make_app()
    app.handle("set Tokyo, JP", sender="+440001111111")
    response = app.handle("", sender="+440002222222")
    assert "UTC" in response


@patch.object(DateApp, "_lookup_timezone", return_value=None)
def test_invalid_city_returns_error(mock_tz):
    app = make_app()
    response = app.handle("Xyzzyville", sender="+440001111111")
    assert "could not find" in response.lower() or "not found" in response.lower()


@patch.object(DateApp, "_lookup_timezone", return_value="Europe/London")
def test_response_contains_date_components(mock_tz):
    app = make_app()
    response = app.handle("London", sender="+440001111111")
    assert ":" in response  # time separator
    assert "202" in response  # year


@patch.object(DateApp, "_lookup_timezone", return_value="Europe/London")
def test_set_default_persists_to_file(mock_tz, tmp_path):
    app = make_app(tmp_path)
    app.handle("set London, GB", sender="+440001111111")
    data = json.loads((tmp_path / "date_defaults.json").read_text())
    assert data["+440001111111"] == "London, GB"


@patch.object(DateApp, "_lookup_timezone", return_value="Asia/Tokyo")
def test_defaults_loaded_from_file_on_init(mock_tz, tmp_path):
    (tmp_path / "date_defaults.json").write_text(json.dumps({"+440001111111": "Tokyo, JP"}))
    app = make_app(tmp_path)
    response = app.handle("", sender="+440001111111")
    assert "Tokyo" in response


@patch.object(DateApp, "_lookup_timezone", return_value="Europe/London")
def test_no_data_dir_still_works(mock_tz):
    app = DateApp()
    app.handle("set London, GB", sender="+440001111111")
    response = app.handle("", sender="+440001111111")
    assert "London" in response
