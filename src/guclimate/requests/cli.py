import typer
import inquirer
from ..core import ui
import os
import logging
import requests
from datapi import ApiClient
from .shortcuts import ecv

from .download import CdsDownload
from .transform import CdsTransformer

app = typer.Typer(
    help="Make and view requests in the Copernicus Climate Data Store (CDS)"
)

logging.basicConfig(level="CRITICAL")
logging.getLogger("processing").setLevel("CRITICAL")


@app.command(help="Create new request", name="new")
def new_request():
    chosen_template = inquirer.list_input(
        message="Which data would you like to request?",
        choices=[
            (
                "Anomaly data from the 'ecv-for-climate-change' dataset",
                "anomalies",
            ),
            (
                "Monthly means from the 'ecv-for-climate-changes' dataset",
                "monthly-means",
            ),
        ],
    )

    if chosen_template == "anomalies":
        request = ecv.anomlies()
    elif chosen_template == "monthly-means":
        request = ecv.monthly_means()

    request.print()

    confirm = inquirer.confirm(
        message="Would you like to submit this request?",
    )

    if not confirm:
        return

    try:
        client = ApiClient(progress=False)
        client.submit(collection_id=request.product, request=request.params)

        ui.success("Request submitted to CDS.", after="\n\n")

        print(
            f"You can view and download requests using {
                ui.color('blue', 'guclimate requests list')},"
            + " or at https://cds.climate.copernicus.eu/requests.\n"
        )

    except requests.HTTPError as err:
        response = err.response.json()

        ui.error("Request rejected by CDS. Here's what they said:")

        print('"' + response["detail"] + '"')

    except Exception as err:
        ui.error("Request unexpectedly failed.")
        print(err)


@app.command(help="List requests", name="list")
def list_requests():
    client = ApiClient(progress=False)

    job_choices = []
    longest_name_chars = 0

    jobs = client.get_jobs().response.json()["jobs"]

    for job in jobs:
        del job["links"]

        if "datasetMetadata" in job:
            del job["datasetMetadata"]

        job["parameters"] = client.get_remote(job["jobID"]).request

        name_and_variable = format_job_dataset_variable(job)

        if len(name_and_variable) > longest_name_chars:
            longest_name_chars = len(name_and_variable)

    for job in jobs:
        name_and_variable = format_job_dataset_variable(job)
        name_and_variable += " " * (longest_name_chars - len(name_and_variable) + 3)

        formatted_job = (
            name_and_variable
            + format_job_status(job)
            + " "
            + format_iso_date(job["created"])
        )

        job_choices.append(
            (
                formatted_job,
                job,
            )
        )

    chosen_job = inquirer.list_input(
        message="Select a CDS request",
        choices=job_choices,
    )

    chosen_action = inquirer.list_input(
        message="What would you like to do with this request?",
        choices=[
            ("Download", "download"),
            (
                f"{ui.color('grey', 'Store in S3')}   {ui.badge('grey', 'Coming soon')}",
                "s3",
            ),
        ],
        validate=lambda _, answer: answer != "s3",
    )

    if chosen_action == "download":
        chosen_format = inquirer.list_input(
            message="What format should this download be in?",
            choices=[
                ("GRIB", "grib"),
                ("NetCDF", "nc"),
                ("CSV", "csv"),
            ],
        )

        job_variable = chosen_job["parameters"]["variable"]

        if isinstance(job_variable, list):
            job_variable = job_variable[0]

        filename = inquirer.text(
            message="What will this file be called?",
            default=f"{job_variable}.{chosen_format}",
        )

        if not filename.endswith(chosen_format):
            filename += chosen_format

        full_download_path = os.getcwd() + "/" + filename

        with CdsDownload(client, chosen_job["jobID"]) as download:
            print("\nWorking on it...\n")

            download.download()

            with CdsTransformer(download) as transformer:
                if chosen_format == "grib":
                    result = transformer.save_as("grib", full_download_path)
                elif chosen_format == "nc":
                    result = transformer.save_as("nc", full_download_path)
                else:
                    result = transformer.save_as("csv", full_download_path)

                if result["files_created"] > 1:
                    ui.success(
                        f"'{result['filename']}' folder successfully created, "
                        + f"containing {result['files_created']} files."
                        + " Run [blue]open .[/blue] to see the file in Finder",
                        before="\n",
                    )
                else:
                    ui.success(
                        f"'{result['filename']}' successfully created."
                        + " Run [blue]open .[/blue] to see the file in Finder",
                        before="\n",
                    )


def format_job_dataset_variable(job):
    variable = job["parameters"]["variable"]

    if isinstance(variable, list):
        variable = variable[0]

    return job["processID"] + f" ({variable}) "


def format_job_status(job):
    if (
        job["status"] == "successful"
        and job.get("metadata")
        and job["metadata"].get("results")
        and job["metadata"]["results"].get("type")
        and job["metadata"]["results"]["type"] == "results expired"
    ):
        return ui.color("grey", "∅ Expired   ")

    if job["status"] == "successful":
        return ui.color("green", "✔ Complete  ")

    if job["status"] == "accepted" or job["status"] == "running":
        return ui.color("yellow", "⏺︎ Running  ")

    if job["status"] == "failed":
        return ui.color("red", "✗ Failed    ")

    return ui.color("red", "⏺︎ Unknown  ")


def format_iso_date(date):
    return date.split("T")[0] + " " + date.split("T")[1].split(".")[0]
    return date.split("T")[0] + " " + date.split("T")[1].split(".")[0]
