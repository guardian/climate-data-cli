import inquirer
import typer
import requests
from datapi import ApiClient
from rich import print
import os

from ..core import ui

app = typer.Typer(
    help="Walk through the setup steps needed to connect to CDS on this machine"
)


@app.callback(invoke_without_command=True)
def setup():
    ui.message("First, create an ECMWF account.", after="\n\n")

    print("Create an account at [blue]https://www.ecmwf.int/user/login[/blue].\n")

    print(
        "Once you've created your account, visit "
        + "[blue]https://cds.climate.copernicus.eu/profile[/blue], and copy your API token.\n"
    )

    api_key = inquirer.password(message="Enter your API key")
    print("")

    ui.message("Verifying your key with CDS...", after="\n\n")

    client = ApiClient(key=api_key)

    try:
        client.check_authentication()
    except requests.HTTPError as err:
        ui.error("CDS rejected this key. Here's what they said:", after="\n\n")
        print(err)

        raise typer.Exit(0)

    except Exception as err:
        ui.error("Verification unexpectedly failed.", after="\n\n")
        print(err)

        raise typer.Exit(1)

    ui.success(
        "Key is valid! You may now create and access CDS requests with this tool.",
        after="\n\n",
    )

    print(
        "Your key has been stored in a '.datapirc' in your home folder for future use."
    )

    key = f"url: https://cds.climate.copernicus.eu/api\nkey: {api_key}"

    home_dir = os.path.expanduser("~")
    file_path = os.path.join(home_dir, ".datapirc")

    with open(file_path, "w") as file:
        file.write(key)

    os.chmod(file_path, 0o700)
