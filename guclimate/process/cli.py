from typing_extensions import Annotated
from pathlib import Path
from guclimate.core import dataset
import typer
import os
import pandas

app = typer.Typer(help="Retrieve data from the Copernicus Climate Data Store (CDS)")


def validateInputPath(path: str):
    if not os.path.exists(path):
        raise typer.BadParameter(f"Path does not exist: {path}")
    return path


@app.command(help="Generate time series")
def timeseries(
    input: Annotated[
        Path,
        typer.Argument(
            help="Path to source data, e.g. ./dataset.nc",
            callback=validateInputPath,
        ),
    ],
    variable: Annotated[
        str,
        typer.Argument(help="Variable name"),
    ],
    outdir: Annotated[
        Path,
        typer.Argument(
            help="Output directory",
        ),
    ] = "./",
):
    ds = dataset.open_dataset(input)
    ds = ds.global_mean(variable)
    df = ds.timeseries(variable)
    df.to_excel(os.path.join(outdir, "timeseries.xlsx"))
