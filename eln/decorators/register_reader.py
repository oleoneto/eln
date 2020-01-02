# eln:decorators


READERS = dict()


# Decorator for adding reader functions
def register_reader(function):
    READERS[function.__name__] = function
    return function
