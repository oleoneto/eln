import click
from eln.commands.forecast import providers


@click.group()
@click.option('-p', 'provider', type=str, help='Your api provider.')
@click.pass_context
def forecast(ctx, provider):
    """Weather forecast service."""


@forecast.command()
@click.pass_context
def today(ctx):
    """View today's forecast."""


@forecast.command()
@click.pass_context
def tomorrow(ctx):
    """View tomorrow's forecast."""


@forecast.command()
@click.pass_context
def yesterday(ctx):
    """View yesterday's forecast."""


@forecast.command()
@click.pass_context
def week(ctx):
    """View forecast for current week."""
