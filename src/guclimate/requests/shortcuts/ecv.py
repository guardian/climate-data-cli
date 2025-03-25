import inquirer
from .. import validate
from ...core import requests, ui


def anomlies():
    answers = collect_ecv_answers()

    # CDS expects all parameters to be arrays, even if they're single values
    answers["variable"] = [answers["variable"]]
    answers["time_aggregation"] = [answers["time_aggregation"]]
    answers["climate_reference_period"] = [answers["climate_reference_period"]]

    return requests.createCDSRequest(
        {
            "product": "ecv-for-climate-change",
            "product_type": ["anomaly"],
            "origin": ["era5"],
            **answers,
        }
    )


def monthly_means():
    answers = collect_ecv_answers()

    # CDS expects all parameters to be arrays, even if they're single values
    answers["variable"] = [answers["variable"]]
    answers["time_aggregation"] = [answers["time_aggregation"]]
    answers["climate_reference_period"] = [answers["climate_reference_period"]]

    return requests.createCDSRequest(
        {
            "product": "ecv-for-climate-change",
            "product_type": ["monthly_mean"],
            "origin": ["era5"],
            **answers,
        }
    )


def collect_ecv_answers():
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
            "time_aggregation",
            message="Aggregation type?",
            choices=[
                ("Monthly means", "1_month_mean"),
                ("12 month running mean", "12_month_running_mean"),
            ],
        ),
        inquirer.List(
            "climate_reference_period",
            message="Climate reference period",
            choices=[
                ("1991-2020", "1991_2020"),
                ("1981-2010", "1981_2010"),
                (
                    f"{ui.color('grey', '1850-1900')}   {ui.badge('grey', 'Coming soon')}",
                    "1850_1900",
                ),
            ],
            validate=lambda _, answer: answer != "1850_1900",
        ),
        inquirer.Text(
            name="year",
            message="Which year(s) are you interested in? (eg. '1979-2023' or '2022,2023')",
            validate=validate.combineOR(
                [
                    validate.isInteger,
                    validate.isYearRange,
                    validate.isCommaSeparatedIntegers,
                ],
                "Input not valid for variable 'years'",
            ),
            default="1990",
        ),
        inquirer.Text(
            name="month",
            message="Which months(s) are you interested in? (eg. '01-12' or '04,05')",
            validate=validate.combineOR(
                [
                    validate.isInteger,
                    validate.isMonthRange,
                    validate.isCommaSeparatedIntegers,
                ],
                "Input not valid for variable 'months'",
            ),
            default="06",
        ),
    ]

    return inquirer.prompt(questions)
