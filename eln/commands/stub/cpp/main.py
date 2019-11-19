import click


@click.command()
@click.argument('name', required=True)
@click.argument('classes', nargs=-1, required=False)
@click.pass_context
def cpp(ctx, name, classes):
    """
        Stubs out a sample C++ app.
    """

    helper = ctx.obj['helper']

    helper.create_cpp_project(project=name, classes=classes)
