from typing import Optional
import typer

from . import __app_name__, __version__, requests, setup
from .core import dataset


app = typer.Typer()
# app.add_typer(recipes.app, name="recipes")
app.add_typer(requests.app, name="requests")
app.add_typer(setup.app, name="setup")


def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"{__app_name__} v{__version__}")
        raise typer.Exit()


@app.callback()
def main(
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        help="Show the application's version and exit.",
        callback=_version_callback,
        is_eager=True,
    )
) -> None:
    return


@app.command(help="Print a summary of a given dataset")
def inspect(path: str):
    ds = dataset.open_dataset(path)
    ds.inspect()
