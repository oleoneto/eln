from click.testing import CliRunner
from eln.commands.events.main import search


def test_search():
    runner = CliRunner()
    result = runner.invoke(search, 'luanda')
    assert result.exit_code == 0
