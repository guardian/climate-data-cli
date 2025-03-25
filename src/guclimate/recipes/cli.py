from typing_extensions import Annotated
from pathlib import Path
import typer
import yaml
import os
from guclimate.retrieve import cds
from guclimate.core import dataset, requests
from guclimate.core.recipe import Recipe
from guclimate.core.runner import Runner

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
    ],
):
    with open(path, "r") as file:
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
):
    with open(path, "r") as file:
        recipe_yaml = yaml.safe_load(file)
        recipe = Recipe(recipe_yaml)
        runner = Runner(recipe)
        print("----------------------------")
        print("Running recipe...")
        runner.run()
        return

        retrievals = [key for key in recipe["retrieve"]]
        data = {}
        for key in retrievals:
            retrieval = recipe["retrieve"][key]
            output = retrieval["output"]

            print("----------------------------")
            print(f"Retrieving '{key}'")

            if Path(output).is_file():
                print(f"Output file exists: {output}")
                print(f"Skipping retrieval")
                data[key] = output
                print("----------------------------")
                continue

            originalRequest = requests.createCDSRequest(retrieval)

            allRequests = [
                requestByDay
                for requestByYear in originalRequest.splitByYear()
                for requestByMonth in requestByYear.splitByMonth()
                for requestByDay in requestByMonth.splitByDay()
            ]
            print(f"Number of requests: {len(allRequests)}")
            for request in allRequests:
                print(
                    f"Request for days {request.getDays()}, months {request.getMonths()}, years {request.getYears()}"
                )
                filename = f"data_{request.getYears()[0]}_{request.getMonths()[0]}_{request.getDays()[0]}.grib"
                target = Path(output) / filename
                print(f"Output: {target}")
                cds.retrieve(requestByYear, target)
                # data[key] = output
                print("----------------------------")

        if "process" not in recipe:
            print("No processing steps specified")
            return

        processing = [key for key in recipe["process"]]
        for key in processing:
            step = recipe["process"][key]
            print(f"Processing '{key}'")
            input = step["data"]
            if data[input] is None:
                raise ValueError(f"Input data for '{key}' is not available")

            variable = step["variable"]
            if variable is None:
                raise ValueError(f"Variable for '{key}' is not specified")

            output = step["output"]
            if output is None:
                raise ValueError(f"Output for '{key}' is not specified")

            ds = dataset.open_dataset(data[input])
            ds = ds.global_mean(variable)
            df = ds.timeseries(variable)
            df.to_excel(output)

            print("----------------------------")
