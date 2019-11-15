import click
# from eln.commands import
# from eln.commands import
# from eln.commands import


class AliasedGroup(click.Group):
    """
    Adds support for abbreviated commands
    """
    def get_command(self, ctx, cmd_name):
        rv = click.Group.get_command(self, ctx, cmd_name)
        if rv is not None:
            return rv
        matches = [x for x in self.list_commands(ctx)
                   if x.startswith(cmd_name)]
        if not matches:
            return None
        elif len(matches) == 1:
            return click.Group.get_command(self, ctx, matches[0])
        ctx.fail('Too many matches: %s' % ', '.join(sorted(matches)))


@click.command(cls=AliasedGroup)
@click.pass_context
def main(ctx):
    """
        eln: by Leo Neto (Lehvitus ÖU)

        A command-line tool for quick math computations
    """

    # Note for contributors:
    #
    # Commands should be added as sub-commands of the main click group.
    # This enables sub-command chaining. For example:
    #       Add `create` command to `main`:
    #
    #       main.add_command(create)
    #
    #       Then, run:
    #       eln create create-sub-command`


# main.add_command(addition)
# main.add_command(subtraction)
# main.add_command(multiplication)
# main.add_command(division)
# main.add_command(conversion)
# main.add_command(weather)
# main.add_command(time)

if __name__ == '__main__':
    main()
