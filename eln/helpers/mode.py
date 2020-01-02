# helpers:mode

from enum import Enum, auto


class Mode(Enum):

    def _generate_next_value_(name, start, count, last_values):
        return name.capitalize()

    Debug = 'debug'
    Normal = 'normal'
    Verbose = 'verbose'
