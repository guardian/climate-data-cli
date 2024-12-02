from typing_extensions import Annotated
from pathlib import Path
from tabulate import tabulate
import typer
import yaml
import os
from guclimate.retrieve import cds
from guclimate.retrieve.parse_input import createCDSRequest


app = typer.Typer(help="Create and run recipes for common tasks")

def validateInputPath(path: str):
    if not os.path.exists(path):
        raise typer.BadParameter(f"Path does not exist: {path}")
    return path

@app.command(help="Print a summary of a given recipe")
def inspect(
    path: Annotated[
        Path,
        typer.Argument(
            help="Path to recipe file, e.g. ./my_recipe.yaml",
            callback=validateInputPath,
        ),
    ]
):
    with open(path, 'r') as file:
        recipe = yaml.safe_load(file)
        print("----------------------------")
        print(f"Recipe: {recipe['name']}")
        print(f"Description: {recipe['description']}", end="\n\n")
        print(f"Retrieve: {list(recipe['retrieve'].keys())}")
        print("----------------------------")


@app.command(help="Run a given recipe")
def run(
    path: Annotated[
        Path,
        typer.Argument(
            help="Path to recipe file, e.g. ./my_recipe.yaml",
            callback=validateInputPath,
        ),
    ],
    output: Annotated[
        Path,
        typer.Option(
            "--output", 
            "-o",
            prompt="Where do you want store the data, e.g. (./output/monthly-means.nc)",
            help="Where to store the data, e.g. (./anomalies.nc)",
        ),
    ]
):
    with open(path, 'r') as file:
        recipe = yaml.safe_load(file)
        retrievals = [key for key in recipe["retrieve"]]
        for key in retrievals:
            retrieval = recipe["retrieve"][key]
            request = createCDSRequest(retrieval)
            print(f"Request {request.params}")
            cds.retrieve(request, output)
            print("----------------------------")
