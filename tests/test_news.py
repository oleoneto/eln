from click.testing import CliRunner
from eln.commands.news.main import (
    all,
    headlines,
    sources
)


def test_all_news():
    runner = CliRunner()
    result = runner.invoke(all)
    assert result.exit_code == 0


def test_headlines_news():
    runner = CliRunner()
    result = runner.invoke(headlines)
    assert result.exit_code == 0


def test_sources_news():
    runner = CliRunner()
    result = runner.invoke(sources)
    assert result.exit_code == 0
