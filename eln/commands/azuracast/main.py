import click
from eln.commands.azuracast.client import AzuraClient
from eln.helpers.logger import log_error


@click.group()
@click.option('--token', envvar='AZURACAST_API_KEY')
@click.pass_context
def azuracast(ctx, token):
    """
        Manage your Azuracast installation.
    """

    if not token:
        log_error("Missing AZURACAST_API_KEY in environment.")
        raise click.Abort

    ctx.ensure_object(dict)
    ctx.obj['client'] = AzuraClient(api_token=token)


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
