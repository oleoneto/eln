# decorators:weather_provider


PROVIDERS = dict()


def weather_provider(function):
    PROVIDERS[function.__name__] = function
    return function
