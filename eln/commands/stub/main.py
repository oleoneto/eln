import click
import os
from .helpers import CreatorHelper
from .bottle import bottle
from .cpp import cpp
from .package import package


@click.group()
@click.option('--dry', is_flag=True, help='Keep file system intact.')
@click.option('--force', is_flag=True, help='Forcefully run commands.')
@click.pass_context
def stub(ctx, dry, force):
    """
        Stub out sample projects.
    """

    ctx.ensure_object(dict)
    ctx.obj['dry'] = dry
    ctx.obj['force'] = force if not dry else False
    ctx.obj['helper'] = CreatorHelper(path=os.getcwd(), dry=dry, force=force)


stub.add_command(bottle)
stub.add_command(cpp)
stub.add_command(package)
