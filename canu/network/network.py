import click
from click_help_colors import HelpColorsGroup

from .firmware import firmware


@click.group(
    cls=HelpColorsGroup,
    help_headers_color="yellow",
    help_options_color="blue",
)
@click.pass_context
def network(ctx):
    """Check out the entire network"""
    pass


network.add_command(firmware.firmware)