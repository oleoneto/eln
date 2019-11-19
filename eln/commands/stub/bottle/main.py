import click


@click.command()
@click.argument('name', required=True)
@click.pass_context
def bottle(ctx, name):
    """
        Stubs out a sample Bottle app.
    """

    helper = ctx.obj['helper']

    helper.create_bottle_app(project=name)
