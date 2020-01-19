# weather:client

import requests
from enum import Enum, auto, unique
from datetime import datetime
from gettext import gettext as _
from eln.helpers.time import Week
from eln.decorators import timed


@unique
class Unit(Enum):
    def _generate_next_value_(name, start, count, last_values):
        return name

    Celsius = auto()
    Fahrenheit = auto()
    Kelvin = auto()


@unique
class WeatherScope(Enum):
    def _generate_next_value_(name, start, count, last_values):
        return name

    Weather = auto()
    Forecast = auto()


WEATHER_TODAY = \
    """
    {description}
    {temperature} {unit} - Wind {wind_speed} m/s
    Humidity {humidity}%
    Sunrise {sunrise} - Sunset {sunset}
    Low: {min_temperature} {unit}
    High: {max_temperature} {unit}
    """

WEATHER_FORECAST = \
    """
    {date}
    {description}
    {temperature} {unit} - Wind {wind_speed} m/s
    Low: {min_temperature} {unit}
    High: {max_temperature} {unit}
    """


class WeatherClient:

    def __init__(self, api_key, location, language, unit):
        self.__api_key = api_key
        self.__location = location
        self.__language = language
        self.__unit = unit
        self.__query = 'id=' if self.__location.isnumeric() else 'q='
        self.__scope = 'weather'
        self.__endpoint = 'https://api.openweathermap.org/data/2.5/{scope}?{query}{location}&lang={language}&APPID={api_key}'

    def _convert_temperature(self, temperature):
        # Converts temperature from K to Celsius or Fahrenheit
        if self.__unit == Unit.Celsius:
            return float(round(temperature - 273.15, 1))
        elif self.__unit == Unit.Fahrenheit:
            return float(round((temperature - 273.15) * 9 / 5 + 32, 1))

        return temperature

    def get_weather(self):
        req = requests.get(
            self.__endpoint.format(
                scope='weather',
                query=self.__query,
                location=self.__location,
                language=self.__language,
                api_key=self.__api_key
            )
        )
        res = req.json()

        temperature = self._convert_temperature(res['main']['temp'])
        min_temperature = self._convert_temperature(res['main']['temp_min'])
        max_temperature = self._convert_temperature(res['main']['temp_max'])

        return WEATHER_TODAY.format(
            unit=self.__unit.value,
            description=res['weather'][0]['description'].title(),
            temperature=temperature,
            min_temperature=min_temperature,
            max_temperature=max_temperature,
            humidity=res['main']['humidity'],
            wind_speed=res['wind']['speed'],
            sunrise=datetime.fromtimestamp(res['sys']['sunrise']).time(),
            sunset=datetime.fromtimestamp(res['sys']['sunset']).time(),
        ), res['name']

    def get_forecast(self):
        req = requests.get(
            self.__endpoint.format(
                scope='forecast',
                query=self.__query,
                location=self.__location,
                language=self.__language,
                api_key=self.__api_key
            )
        )
        res = req.json()

        weather_forecast = []

        for index, day in enumerate(res['list']):
            temperature = self._convert_temperature(day['main']['temp'])
            min_temperature = self._convert_temperature(day['main']['temp_min'])
            max_temperature = self._convert_temperature(day['main']['temp_max'])
            date = day['dt_txt']
            weekday = list(Week)[datetime.fromisoformat(date).weekday()]

            weather_forecast.append(
                WEATHER_FORECAST.format(
                    date=f"{weekday.value} - {date}",
                    unit=self.__unit.value,
                    description=day['weather'][0]['description'].title(),
                    temperature=temperature,
                    min_temperature=min_temperature,
                    max_temperature=max_temperature,
                    wind_speed=day['wind']['speed'],
                )
            )

        return weather_forecast, res['city']['name']
