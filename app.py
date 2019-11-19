import click
from eln.commands.news import news
from eln.commands.azuracast import azuracast
from eln.commands.stub import stub
from eln.commands.digitalocean import digitalocean
from dotenv import load_dotenv


load_dotenv()


__author__ = 'Leo Neto'


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
@click.version_option()
@click.pass_context
def main(ctx):
    """
        eln: by Leo Neto (Lehvitus ÖU)

        A command-line tool for quick access to web services
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


main.add_command(news)
main.add_command(azuracast)
main.add_command(stub)
main.add_command(digitalocean)

if __name__ == '__main__':
    main()
