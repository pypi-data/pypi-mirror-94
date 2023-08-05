from typing import Optional

import click

from lean.api.api_client import APIClient
from lean.config.global_config import api_token_option, user_id_option
from lean.constants import GLOBAL_CONFIG_DIR


@click.command()
@click.option("--user-id", "-u", type=str, help="QuantConnect.com user id")
@click.option("--api-token", "-t", type=str, help="QuantConnect.com API token")
def login(user_id: Optional[str], api_token: Optional[str]) -> None:
    """Log in with a QuantConnect account.

    If user id or API token is not provided an interactive prompt will show.

    Credentials are stored in ~/.lean/credentials and are removed upon running `lean logout`.
    """
    if user_id is None or api_token is None:
        click.echo("Your user id and API token are needed to make authenticated requests to the QuantConnect API")
        click.echo("You can request these credentials on https://www.quantconnect.com/account")
        click.echo(f"Both will be saved in ~/{GLOBAL_CONFIG_DIR}/{user_id_option.file_name}")

    if user_id is None:
        user_id = click.prompt("User id")

    if api_token is None:
        api_token = click.prompt("API token")

    api_client = APIClient(user_id, api_token)

    if not api_client.is_authenticated():
        raise click.ClickException("Credentials are invalid")

    user_id_option.set_value(user_id)
    api_token_option.set_value(api_token)

    click.echo("Successfully logged in")
