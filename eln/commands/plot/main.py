import click
import pathlib
from matplotlib import pyplot as plt
from eln.commands.plot import readers


def __read_data(file_path):
    """Transform data into Pandas DataFrame"""
    file_format = file_path.suffix.lstrip('.')
    return readers.read(file_format, file_path)


def __create_plot(data):
    """Plot a Pandas DataFrame"""
    data.plot()
    plt.show()


@click.command()
@click.pass_context
@click.argument('file_path')
def plot(ctx, file_path):
    """Plot Pandas DataFrame."""
    file_path = pathlib.Path(file_path)
    data = __read_data(file_path)
    __create_plot(data)
