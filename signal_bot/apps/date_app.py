import json
from collections.abc import Iterator
from datetime import datetime, timezone
from pathlib import Path
from zoneinfo import ZoneInfo
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
from signal_bot.app_interface import CommandApp


class DateApp(CommandApp):
    def __init__(self, data_dir: Path | str | None = None) -> None:
        self._geolocator = Nominatim(user_agent="signal-bot-date-app")
        self._tf = TimezoneFinder()
        self._data_dir = Path(data_dir) if data_dir is not None else None
        self._defaults: dict[str, str] = self._load_defaults()

    @property
    def name(self) -> str:
        return "date"

    @property
    def description(self) -> str:
        return "Shows date/time for a city. Use /date set City, Country to save a default"

    def handle(self, args: str, sender: str = "") -> Iterator[str]:
        stripped = args.strip()
        if stripped.lower().startswith("set "):
            yield self._set_default(stripped[4:].strip(), sender)
            return
        if stripped:
            yield self._date_for_city(stripped)
            return
        if sender in self._defaults:
            yield self._date_for_city(self._defaults[sender])
            return
        yield self._format_utc()

    def _defaults_path(self) -> Path | None:
        if self._data_dir is None:
            return None
        return self._data_dir / "date_defaults.json"

    def _load_defaults(self) -> dict[str, str]:
        path = self._defaults_path()
        if path is None or not path.exists():
            return {}
        with open(path) as f:
            return json.load(f)

    def _save_defaults(self) -> None:
        path = self._defaults_path()
        if path is None:
            return
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w") as f:
            json.dump(self._defaults, f)

    def _set_default(self, location: str, sender: str) -> str:
        tz_name = self._lookup_timezone(location)
        if tz_name is None:
            return f"Could not find location: {location}"
        city = location.split(",")[0].strip()
        self._defaults[sender] = location
        self._save_defaults()
        return f"Default set to {city}."

    def _date_for_city(self, location: str) -> str:
        tz_name = self._lookup_timezone(location)
        if tz_name is None:
            return f"Could not find location: {location}"
        city = location.split(",")[0].strip()
        tz = ZoneInfo(tz_name)
        now = datetime.now(tz)
        return f"{city}: {now.strftime('%A %Y-%m-%d %H:%M:%S %Z')}"

    def _lookup_timezone(self, location: str) -> str | None:
        try:
            result = self._geolocator.geocode(location)
        except Exception:
            return None
        if result is None:
            return None
        return self._tf.timezone_at(lng=result.longitude, lat=result.latitude)

    def _format_utc(self) -> str:
        now = datetime.now(timezone.utc)
        return f"UTC: {now.strftime('%A %Y-%m-%d %H:%M:%S %Z')}"
