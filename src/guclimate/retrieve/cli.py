import typer
import inquirer
import json
import os
from . import validate, parse_input, cds
from typing_extensions import Annotated
from pathlib import Path
from tabulate import tabulate

app = typer.Typer(help="Retrieve data from the Copernicus Climate Data Store (CDS)")

def validatePath(path: str):
    outputDir = os.path.dirname(path)
    if not os.path.exists(outputDir):
        raise typer.BadParameter(f"Output directory '{outputDir}' does not exist")
    return path

@app.command(help="Verify CDS credentials")
def verify():
    print("Verifying CDS credentials")
    response = cds.verify()
    print("Credentials verified", response)


@app.command(help="List available products from the Climate Data Store (CDS)")
def list():
    products = cds.getProducts()
    productList = [[product["title"], product["id"]] for product in products]
    # products = [[key, cds.products[key]] for key in cds.products]
    print(
        tabulate(
            productList,
            headers=["Name", "Identifier"],
            tablefmt="simple_grid",
            maxcolwidths=[50, None],
        ),
        end="\n\n",
    )


@app.command(help="Retrieve dataset from the Climate Data Store (CDS)")
def product(
    identifier: Annotated[
        str,
        typer.Argument(help="The product identifier"),
    ],
    productType: Annotated[str, typer.Option(help="The product type")] = "",
    variable: Annotated[str, typer.Option(help="The variable in the dataset")] = "",
):
    print(f"Retrieving dataset '{identifier}'")
    print(f"Product type: '{productType}'")
    print(f"Variable: {variable}")


@app.command(help="Anomaly data from the 'ecv-for-climate-change' dataset")
def anomalies(
    output: Annotated[
        Path,
        typer.Argument(
            help="Where to store the data, e.g. (./anomalies.nc)", callback=validatePath
        ),
    ]
):
    questions = [
        inquirer.List(
            "variable",
            message="Which variable are you interested in?",
            choices=[
                ("Surface air temperature", "surface_air_temperature"),
                ("Precipitation", "precipitation"),
                ("Sea-ice cover", "sea_ice_cover"),
            ],
        ),
        inquirer.List(
            "aggregation",
            message="Aggregation type?",
            choices=[
                ("Monthly means", "1_month_mean"),
                ("12 month running mean", "12_month_running_mean"),
            ],
        ),
        inquirer.Text(
            name="years",
            message="Which year(s) are you interested in? Define a range (e.g. 1979-2023) or a comma-separated list of values (e.g. 2023, 2022)",
            validate=validate.combineOR(
                [
                    validate.isInteger,
                    validate.isYearRange,
                    validate.isCommaSeparatedIntegers,
                ],
                "Input not valid for variable 'years'",
            ),
        ),
        inquirer.Text(
            name="months",
            message="Which months(s) are you interested in? Define a range (e.g. 01-12) or a comma-separated list of values (e.g. 09,10)",
            validate=validate.combineOR(
                [
                    validate.isInteger,
                    validate.isMonthRange,
                    validate.isCommaSeparatedIntegers,
                ],
                "Input not valid for variable 'months'",
            ),
        ),
    ]
    answers = inquirer.prompt(questions)
    # print(f"Answers {answers}")
    request = parse_input.createECVRequest("anomaly", answers)
    print(f"Sending request with parameters: {json.dumps(request.params(), indent=2)}")
    cds.retrieve(request, output)


@app.command(help="Monthly means from the 'ecv-for-climate-change' dataset")
def monthlymeans(
    output: Annotated[
        Path,
        typer.Argument(
            help="Where to store the data, e.g. (./output/monthly-means.nc)",
            callback=validatePath,
        ),
    ]
):
    questions = [
        inquirer.List(
            "variable",
            message="Which variable are you interested in?",
            choices=[
                ("Surface air temperature", "surface_air_temperature"),
                ("Precipitation", "precipitation"),
                ("Sea-ice cover", "sea_ice_cover"),
            ],
        ),
        inquirer.List(
            "aggregation",
            message="Aggregation type?",
            choices=[("Monthly means", "1_month_mean")],
        ),
        inquirer.Text(
            name="years",
            message="Which year(s) are you interested in? Define a range (e.g. 1979-2023) or a comma-separated list of values (e.g. 2023, 2022)",
            validate=validate.combineOR(
                [
                    validate.isInteger,
                    validate.isYearRange,
                    validate.isCommaSeparatedIntegers,
                ],
                "Input not valid for variable 'years'",
            ),
        ),
        inquirer.Text(
            name="months",
            message="Which months(s) are you interested in? Define a range (e.g. 01-12) or a comma-separated list of values (e.g. 09,10)",
            validate=validate.combineOR(
                [
                    validate.isInteger,
                    validate.isMonthRange,
                    validate.isCommaSeparatedIntegers,
                ],
                "Input not valid for variable 'months'",
            ),
        ),
    ]
    answers = inquirer.prompt(questions)
    # print(f"Answers {answers}")
    request = parse_input.createECVRequest("monthly_mean", answers)
    print(f"Sending request with parameters: {json.dumps(request.params(), indent=2)}")
    cds.retrieve(request, output)
