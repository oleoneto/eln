import click


@click.command()
@click.argument('name', required=True)
@click.pass_context
def package(ctx, name):
    """
        Stubs out a Python package.
    """

    helper = ctx.obj['helper']

    helper.create_package(name)
