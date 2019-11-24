from click.testing import CliRunner
from eln.commands.azuracast.main import (
    notify,
    now_playing,
    stations
)


def test_stations():
    runner = CliRunner()
    result = runner.invoke(stations)
    assert result.exit_code == 0


def test_now_playing():
    runner = CliRunner()
    result = runner.invoke(now_playing)
    assert result.exit_code == 0


def test_notify():
    runner = CliRunner()
    result = runner.invoke(notify)
    assert result.exit_code == 0
