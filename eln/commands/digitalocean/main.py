import click
import digitalocean as ocean
from eln.helpers.logger import log_error, log_standard


@click.group()
@click.pass_context
@click.option('--token', envvar='DIGITAL_OCEAN_API_KEY')
def digitalocean(ctx, token):
    """
    DigitalOcean Wrapper.

    \b
    A token is required to authenticate with DigitalOcean's API
    Simply run: `export DIGITAL_OCEAN_API_TOKEN=your_api_token`
    from a shell console to export the token to the environment
    """

    if not token:
        log_error("Missing DIGITAL_OCEAN_API_TOKEN in environment.")
        raise click.Abort

    ctx.ensure_object(dict)
    ctx.obj['manager'] = ocean.Manager(token=token)


@digitalocean.command()
@click.pass_context
def account(ctx):
    """
    Manage account information.
    """

    __account = ctx.obj['manager'].get_account()

    log_standard(
        f"""
        Email: {__account.email}
        UUID: {__account.uuid}
        Status: {__account.status}
        """
    )


@digitalocean.command()
@click.pass_context
@click.option('--register', is_flag=True)
def domains(ctx, register):
    """
    Manage domain information.
    """

    __domains = ctx.obj['manager'].get_all_domains()

    # TODO: Handle domain registration
    if register:
        pass

    for d in __domains:
        log_standard(
            f"""Domain name: {d.name}\nDomain TTL: {d.ttl}"""
        )


@digitalocean.command()
@click.pass_context
@click.option('--register', is_flag=True)
def regions(ctx, register):
    """
    Manage region information.
    """

    __regions = ctx.obj['manager'].get_all_regions()

    # TODO: Handle domain registration
    if register:
        pass

    for r in __regions:
        log_standard(
            f"""Region: {r.name}"""
        )


@digitalocean.command()
@click.pass_context
@click.option('--shutdown', help='Turn droplet off', type=int)
@click.option('--inspect', help='Inspect a single droplet', type=int)
@click.option('--start', help='Star a droplet', type=int)
def droplets(ctx, shutdown, inspect, start):
    """
    Manage droplet information
    """

    if inspect:
        try:
            d = ctx.obj['manager'].get_droplet(inspect)
            click.echo(f'{d.name} {d.id}')
            click.echo(f'{d.status}')

            if start:
                d.reboot()
            return True
        except Exception:
            click.echo('Droplet not found.')
            return False

    if start:
        d = ctx.obj['manager'].get_droplet(start)
        d.reboot()
        return True

    __droplets = ctx.obj['manager'].get_all_droplets()

    if shutdown:
        if shutdown >= len(__droplets):
            click.echo('No droplet to be shut down.')
            return True

        __droplets[shutdown].shutdown()
        click.echo(f'Shut down {__droplets[shutdown].name} - {__droplets[shutdown].id}')

    for d in __droplets:
        log_standard(
            f"""Droplet id: {d.id}\nDroplet name: {d.name}\nStatus: {d.status}
            """
        )


@digitalocean.command()
@click.pass_context
def images(ctx):
    """
    Manage image information.
    """

    __images = ctx.obj['manager'].get_my_images()

    for image in __images:
        log_standard(f"{image}")


@digitalocean.command()
@click.pass_context
def certificates(ctx):
    """
    Manage certificates.
    """

    __certificates = ctx.obj['manager'].get_all_certificates()
    click.echo(__certificates)
