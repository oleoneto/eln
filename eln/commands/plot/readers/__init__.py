"""Read data files in different formats"""
import json as jsonlib
import pandas as pd
from eln.decorators.register_reader import register_reader, READERS as _READERS
from eln.helpers.logger import log_error


class UnsupportedFileFormatError(TypeError):
    """Unsupported file format"""


def read(plugin, *args, **kwargs):
    if plugin in _READERS:
        return _READERS[plugin](*args, **kwargs)

    raise UnsupportedFileFormatError()


@register_reader
def csv(file_path):
    """Read CSV file, return DataFrame"""
    return pd.read_csv(file_path)


@register_reader
def json(file_path):
    """Read JSON file, return DataFrame"""
    json_dict = jsonlib.loads(file_path.read_text())
    return pd.DataFrame(json_dict)


# @register_reader
def xlsx(file_path):
    try:
        import xlrd
    except ImportError:
        log_error("Missing 'xlrd' package...")
        exit(1)
    file = pd.read_excel(file_path)
    return csv(file)
