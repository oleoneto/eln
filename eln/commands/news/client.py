import os
import requests
import pyttsx3
from eln.helpers.logger import (
    log_error,
    log_standard
)
from .templates import articles_template, sources_template


class NewsClient:

    def __init__(
            self, api_key=None, debug=False,
            speak=False, headlines_only=True
    ):
        self.__debug = debug
        self.__speak = speak
        self.__headlines_only = headlines_only
        self.__modes = ['articles', 'sources']
        self.__current_mode = self.__modes[0]
        self.__endpoint = f'https://newsapi.org/v2/'
        self.__token = api_key if api_key else os.environ.get('NEWS_API_KEY')
        self.__headers = {'Authorization': 'Bearer {}'.format(self.__token)}
        self.__response = {}
        self.__content = {}
        self.__engine = pyttsx3.init() if speak else None

    def all(self, **kwargs):

        path = self.__endpoint + 'everything'

        url = self.__prepared_url(path, **kwargs)

        return self.__get_response(url)

    def headlines(self, **kwargs):

        path = self.__endpoint + 'top-headlines'

        url = self.__prepared_url(path, **kwargs)

        return self.__get_response(url)

    def sources(self, **kwargs):

        self.__current_mode = self.__modes[1]

        path = f'{self.__endpoint}sources'

        url = self.__prepared_url(path, **kwargs)

        return self.__get_response(url)

    def read(self):
        if self.__current_mode == 'articles':
            self.__read_articles()
        elif self.__current_mode == 'sources':
            self.__read_sources()

    def __read_articles(self):
        for index, article in enumerate(self.__content):
            title = article['title']
            published_at = article['publishedAt']
            author = article['author']
            description = article['description']
            link = article['url']

            message = articles_template.render(
                index=index,
                title=title,
                author=author,
                publication_date=published_at,
                url=link,
            )

            log_standard(message=message)

            if self.__speak:
                self.__engine.say(title, name='news-api')
                self.__engine.runAndWait()

            if not self.__headlines_only:
                log_standard(message=f'\t{description}')
                if self.__speak:
                    self.__engine.say(description, name='news-api')
                    self.__engine.runAndWait()

    def __read_sources(self):
        for source in self.__content:
            name = source['name']
            country = source['country']
            category = source['category']
            description = source['description']

            log_standard(message=sources_template.render(
                name=name,
                country=country,
                category=category,
            ))

            if self.__speak:
                self.__engine.say(name)
                self.__engine.runAndWait()

            if not self.__headlines_only:
                log_standard(message=f'\t{description}')
                if self.__speak:
                    self.__engine.say(description, name='news-api')
                    self.__engine.runAndWait()

    def __prepared_url(self, path, **kwargs):
        return self.__build_query(
            path=path,
            **kwargs
        )

    def __get_response(self, url):

        if not self.__debug:
            self.__response = requests.get(
                url=url,
                headers=self.__headers
            ).json()

            if 'message' in self.__response:
                log_error(message=self.__response['message'])

            if self.__current_mode in self.__response:
                self.__content = self.__response[f'{self.__current_mode}']

        return self.__response

    def __build_query(self, **kwargs):

        path = kwargs.pop('path') if kwargs.get('path') else self.__endpoint

        path += '?'

        for k, v in kwargs.items():

            # Normalize `from` key for url params
            k = "from" if k is "from_" else k

            if v is not None:
                path += f"{k}={v}&"

        if path.endswith('&'):
            path = path.rsplit('&', 1)[0]
        if path.endswith('?'):
            path = path.rsplit('?', 1)[0]

        if self.__debug:
            log_standard(message=f'Request URL: {path}')

        return path
