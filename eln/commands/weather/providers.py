# commands:weather:providers
import requests
from eln.decorators.weather_provider import weather_provider, PROVIDERS


class UnsupportedProviderError(TypeError):
    """Unsupported provider"""


def get_weather(provider, *args, **kwargs):
    if provider in PROVIDERS:
        return PROVIDERS[provider](*args, **kwargs)

    raise UnsupportedProviderError()


@weather_provider
def open_weather(*args, **kwargs):
    """OpenWeatherMap"""


@weather_provider
def dark_sky(*args, **kwargs):
    """DarkSky"""
