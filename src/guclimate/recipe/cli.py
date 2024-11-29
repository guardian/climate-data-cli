from typing_extensions import Annotated
from pathlib import Path
from tabulate import tabulate
import typer
import yaml
import os


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


@app.command(help="Execute a given recipe")
def cook(
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
        retrievals = [key for key in recipe["retrieve"]]
        for key in retrievals:
            request = recipe["retrieve"][key]
            print(f"Request {request}")

