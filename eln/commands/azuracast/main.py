import click
from .client import AzuraClient


@click.group()
@click.pass_context
def azuracast(ctx):
    """
        Manage your Azuracast installation.
    """

    ctx.ensure_object(dict)
    ctx.obj['client'] = AzuraClient()


@azuracast.command()
@click.pass_context
def stations(ctx):
    """
        List your radio stations.
    """
    client = ctx.obj['client']

    client.stations()


@azuracast.command()
@click.pass_context
def now_playing(ctx):
    """
        Show now playing metadata.
    """

    client = ctx.obj['client']

    client.now_playing()


@azuracast.command()
@click.argument('message', required=False)
@click.option('--now-playing', is_flag=True)
@click.pass_context
def notify(ctx, message, now_playing):
    """
        Send station notifications via Telegram.
    """
    client = ctx.obj['client']

    if now_playing:
        client.notify_now_playing()

    else:
        client.notify(message=message)
