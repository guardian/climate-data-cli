from . import __app_name__, __version__, retrieve, process
from .core import dataset
from typing import Optional

import typer

app = typer.Typer()
app.add_typer(retrieve.app, name="retrieve")
app.add_typer(process.app, name="process")

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
