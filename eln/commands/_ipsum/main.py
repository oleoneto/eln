# commands:ipsum
import click


@click.group()
@click.pass_context
def ipsum(ctx):
    """Generate random text samples."""


@ipsum.command
@click.option('-p', '--paragraphs', type=int, help='Number of paragraphs.')
@click.pass_context
def food():
    """Generate food-related text passages."""


@ipsum.command
@click.option('-p', '--paragraphs', type=int, help='Number of paragraphs.')
@click.pass_context
def tv():
    """Generate tv-related text passages."""
