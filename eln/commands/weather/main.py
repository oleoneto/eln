import click
from eln.commands.weather.client import WeatherClient, Unit
from eln.helpers.logger import log_error, log_standard
from gettext import gettext as _


WEATHER_PROVIDER_NOTICE = \
    """
    Data provided by https://openweathermap.org

    Weather for {}
    """


@click.group()
@click.option('--token', envvar='OPEN_WEATHER_API_KEY')
@click.option('-l', '--location', envvar='WEATHER_LOCATION', default='London,UK')
@click.option('--language', envvar='ELN_LANGUAGE', default='en')
@click.option('-u', '--unit', type=click.Choice(['celsius', 'fahrenheit', 'kelvin']), default='fahrenheit')
@click.pass_context
def weather(ctx, token, location, language, unit):
    """Weather and forecast service."""

    unit = Unit(unit.capitalize())

    if not token:
        log_error(_("Missing OPEN_WEATHER_API_KEY in environment."))
        raise click.Abort

    ctx.obj['client'] = WeatherClient(
        api_key=token,
        location=location,
        language=language,
        unit=unit or Unit.Celsius,
    )

    ctx.obj['location'] = location


@weather.command()
@click.pass_context
def today(ctx):
    """Get current weather information."""

    info, location = ctx.obj['client'].get_weather()

    log_standard(WEATHER_PROVIDER_NOTICE.format(location))

    log_standard(info)


@weather.command()
@click.pass_context
def forecast(ctx):
    """Get weather forecast."""

    info, location = ctx.obj['client'].get_forecast()

    log_standard(WEATHER_PROVIDER_NOTICE.format(location))

    for f in info:
        log_standard(f)
