from typing import Optional
from typing_extensions import Annotated

import typer
import inquirer
import json
import pprint

from guclimate import __app_name__, __version__
from guclimate import cds, parse_input, dataset, validate, requests

app = typer.Typer()

pp = pprint.PrettyPrinter(indent=2)


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


@app.command()
def anomalies(output: str):
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
    request = parse_input.createAnomalyRequest(answers)
    print(f"Sending request with parameters: {json.dumps(request.params(), indent=2)}")
    cds.retrieve(request, output)


@app.command()
def inspect(path: str):
    ds = dataset.open_dataset(path)
    print("ds", ds)
    print("global avg anomaly", ds.global_mean())


@app.command()
def store(
    inputdir: str,
    input_name: str,
    output: str,
):
    result = cds.ResultSet(inputdir, input_name, requests.ResultFormat.ZIP)
    pp.pprint(result.files)
    result.save(output)
