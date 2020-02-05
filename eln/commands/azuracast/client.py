import os
import click
from pprint import pprint
import json
import requests
from eln.helpers.logger import log_standard, log_error
from .templates import (
    notification_template,
    tracks_template,
    stations_template,
    slack_message,
)


class AzuraClient:

    def __init__(
            self,
            api_token=None,
            endpoint=None,
            telegram_token=None,
            telegram_chat=None,
            slack_token=None,
    ):
        self.__token = api_token if api_token else os.environ.get('AZURACAST_API_KEY')
        self.__station_endpoint = endpoint if endpoint else os.environ.get('AZURACAST_STATION_ENDPOINT')
        self.__headers = {'X-API-Key': '{}'.format(self.__token)}
        self.__telegram_token = telegram_token if telegram_token else os.environ.get('TELEGRAM_KEY')
        self.__slack_token = slack_token if slack_token else os.environ.get('SLACK_TOKEN')
        self.__telegram_chat = telegram_chat if telegram_chat else os.environ.get('TELEGRAM_CHAT')
        self.__telegram_endpoint = 'https://api.telegram.org/bot{}/sendMessage'.format(self.__telegram_token)
        self.__data = {}
        self.__environment_error = "Missing variables:"

        try:
            self.__ensure_environment_variables()
        except EnvironmentError:
            log_error(self.__environment_error)
            raise click.Abort

    def stations(self):
        url = self.__station_endpoint + 'stations'

        self.__data = requests.get(url, self.__headers).json()

        self.__list_stations()

    def now_playing(self):
        url = self.__station_endpoint + 'nowplaying'

        self.__data = requests.get(url, self.__headers).json()

        self.__list_now_playing()

    def __send_to_slack(self, data):
        url = f'https://hooks.slack.com/services/{self.__slack_token}'
        content = slack_message.render(
            history=data['history'],
            radio=data['name'],
            url=data['url'],
            title=data['title'],
            artist=data['artist'],
        )
        json_content = json.loads(content)
        _ = requests.post(url=url, json=json_content)
        return _.status_code
    
    def __send_to_telegram(self, data):
        try:
            self.__ensure_environment_variables_for_telegram()
        except EnvironmentError:
            log_error(self.__environment_error)
            exit()

        url = self.__telegram_endpoint

        message = notification_template.render(
            name=data['name'],
            url=data['url'],
            title=data['title'],
            artist=data['artist'],
        )

        params = {
            "chat_id": f"{self.__telegram_chat}",
            "text": f"{message}",
            "parse_mode": "Markdown"
        }

        _ = requests.post(url=url, params=params)
        return _.status_code

    def notify(self, avenue, message=None, station=None, force=False):
        if message is None:
            log_error("Message cannot be empty")
            raise click.Abort

        if message.replace(' ', '_') in ['now_playing', 'playing']:
            self.notify_now_playing(avenue=avenue, station=station)

    def notify_now_playing(self, avenue, station=None):
        url = self.__station_endpoint + 'nowplaying'

        self.__data = requests.get(url, self.__headers).json()

        for data in self.__data:
            name = data['station']['name']
            url = data['station']['listen_url']
            now_playing = data['now_playing']
            now = now_playing['song']
            song_history = data['song_history']

            history = [song['song'] for song in song_history]

            check = station is None

            if station is not None:
                comparable_source_name = name.lower().replace(' ', '_')
                comparable_input_name = station.lower().replace(' ', '_')
                check = comparable_input_name == comparable_source_name

            if check:
                data = {
                    'history': history,
                    'name': name,
                    'url': url,
                    'title': now['title'],
                    'artist': now['artist'],
                }

                if avenue in ['all', 'telegram']:
                    self.__send_to_telegram(data=data)
                if avenue in ['all', 'slack']:
                    self.__send_to_slack(data=data)

    def data(self):
        return self.__data

    def __list_now_playing(self):
        for _, data in enumerate(self.__data):
            station = data['station']
            listeners = data['listeners']['total']
            now_playing = data['now_playing']
            song_history = data['song_history']
            name = station['name']
            backend = station['backend']
            frontend = station['frontend']
            listen_url = station['listen_url']

            divider = f"{name} -"

            while len(divider) < 60:
                divider += '-'

            # What is currently playing...
            now = now_playing['song']
            before_0 = song_history[0]['song']
            before_1 = song_history[1]['song']
            before_2 = song_history[2]['song']
            before_3 = song_history[3]['song']
            before_4 = song_history[4]['song']

            message = tracks_template.render(
                divider=divider,
                backend=backend,
                frontend=frontend,
                listeners=listeners,
                url=listen_url,
                main_title=now['title'],
                main_artist=now['artist'],
                title_0=before_0['title'],
                artist_0=before_0['artist'],
                title_1=before_1['title'],
                artist_1=before_1['artist'],
                title_2=before_2['title'],
                artist_2=before_2['artist'],
                title_3=before_3['title'],
                artist_3=before_3['artist'],
                title_4=before_4['title'],
                artist_4=before_4['artist'],
            )
            log_standard(message=message)

    def __list_stations(self):
        for index, station in enumerate(self.__data):

            name = station['name']
            short_code = station['shortcode']
            listen_url = station['listen_url']
            description = station['description']
            backend = station['backend']
            frontend = station['frontend']

            lines = f"{name} -"

            while len(lines) < 60:
                lines += '-'

            message = stations_template.render(
                divider=lines,
                description=description,
                short_code=short_code,
                backend=backend,
                frontend=frontend,
                url=listen_url
            )

            log_standard(message=message)

    def __ensure_environment_variables(self):
        error = False

        if os.environ.get('AZURACAST_API_KEY') is None:
            error = True
            self.__environment_error += "\nAZURACAST_API_KEY"
        if os.environ.get('AZURACAST_STATION_ENDPOINT') is None:
            error = True
            self.__environment_error += "\nAZURACAST_STATION_ENDPOINT"

        if error:
            raise EnvironmentError

    def __ensure_environment_variables_for_telegram(self):
        error = False

        if os.environ.get('TELEGRAM_KEY') is None:
            error = True
            self.__environment_error += "\nTELEGRAM_KEY"
        if os.environ.get('TELEGRAM_CHAT') is None:
            error = True
            self.__environment_error += "\nTELEGRAM_CHAT"

        if error:
            raise EnvironmentError
