import click

from lean.config.global_config import GlobalConfig
from lean.constants import CREDENTIALS_FILE


@click.command()
def logout() -> None:
    """Log out and remove stored credentials."""
    GlobalConfig(CREDENTIALS_FILE).clear()
