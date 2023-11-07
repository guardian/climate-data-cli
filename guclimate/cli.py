from typing import Optional

import typer
import inquirer

from guclimate import __app_name__, __version__
from guclimate import cds, requests

app = typer.Typer()

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
def anomalies():
    questions = [
    inquirer.List('variable',
                    message="Which variable are you interested in?",
                    choices=[("Surface air temperature", "surface_air_temperature"), ("Precipitation", "precipitation"), ("Sea-ice cover", "sea_ice_cover")],
                ),
    inquirer.List('aggregation',
                    message="Aggregation type?",
                    choices=[("Monthly means", "1_month_mean")],
                ),
    # inquirer.Text(name='years', 
    #               message="Which year(s) are you interested in? Define a range (e.g. 1979-2023) or a comma-separated list of values (e.g. 2023, 2022)"),
    # inquirer.Text(name='months', 
    #               message="Which months(s) are you interested in? Define a range (e.g. 01-12) or a comma-separated list of values (e.g. 09,10)"),
    ]
    answers = inquirer.prompt(questions)
    # print(f"Answers {answers}")
    request = requests.AnomalyRequest(answers['variable'])
    # print(f"Request {request.variable}")
    cds.retrieve(request)


