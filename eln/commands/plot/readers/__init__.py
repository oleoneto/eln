"""Read data files in different formats"""
import json as jsonlib
import pandas as pd
from eln.decorators import register_reader, READERS as _READERS


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
