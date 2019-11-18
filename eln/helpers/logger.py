import click


def log_error(message, **kwargs):
    click.secho(message=message, **kwargs, fg='red')


def log_success(message, **kwargs):
    click.secho(message=message, **kwargs, fg='green')


def log_standard(message, **kwargs):
    click.secho(message=message, **kwargs)
