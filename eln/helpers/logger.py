import click


def log_error(**kwargs):
    click.secho(**kwargs, fg='red')


def log_success(**kwargs):
    click.secho(**kwargs, fg='green')


def log_standard(**kwargs):
    click.secho(**kwargs)
