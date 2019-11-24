from click.testing import CliRunner
from eln.commands.stub.main import package, cpp, bottle


def test_stub_package():
    runner = CliRunner()
    with runner.isolated_filesystem():
        result = runner.invoke(package, ['package_name'])
        assert result.exit_code == 0


def test_stub_bottle():
    runner = CliRunner()
    with runner.isolated_filesystem():
        result = runner.invoke(bottle, ['website'])
        assert result.exit_code == 0


def test_stub_cpp():
    runner = CliRunner()
    with runner.isolated_filesystem():
        result = runner.invoke(cpp, ['library', 'book', 'author'])
        assert result.exit_code == 0
