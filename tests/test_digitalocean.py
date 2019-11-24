from click.testing import CliRunner
from eln.commands.digitalocean.main import (
    account,
    certificates,
    domains,
    droplets,
    images,
    regions
)


def test_account():
    runner = CliRunner()
    result = runner.invoke(account)
    assert result.exit_code == 0


def test_certificates():
    runner = CliRunner()
    result = runner.invoke(certificates)
    assert result.exit_code == 0


def test_domains():
    runner = CliRunner()
    result = runner.invoke(domains)
    assert result.exit_code == 0


def test_droplets():
    runner = CliRunner()
    result = runner.invoke(droplets)
    assert result.exit_code == 0


def test_images():
    runner = CliRunner()
    result = runner.invoke(images)
    assert result.exit_code == 0


def test_regions():
    runner = CliRunner()
    result = runner.invoke(regions)
    assert result.exit_code == 0
