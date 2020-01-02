# helpers:time
import inflection
from enum import Enum, auto, unique


@unique
class Time(Enum):

    def _generate_next_value_(name, start, count, last_values):
        return inflection.underscore(name)

    Today = auto()
    Yesterday = auto()
    Tomorrow = auto()
    NextWeek = auto()


@unique
class Week(Enum):

    def _generate_next_value_(name, start, count, last_values):
        return name

    Monday = auto()
    Tuesday = auto()
    Wednesday = auto()
    Thursday = auto()
    Friday = auto()
    Saturday = auto()
    Sunday = auto()
