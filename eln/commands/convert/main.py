import click
from eln.helpers.logger import log_standard
from gettext import gettext as _


@click.group()
@click.argument('value', type=float, required=True)
@click.option('-u', '--unit', required=True)
@click.pass_context
def convert(ctx, value, unit):
    """Convert units of measurement."""

    log_standard(value)


@convert.command
@click.argument('unit', required=True)
@click.pass_context
def to(ctx, unit):
    """_"""

    log_standard(unit)
