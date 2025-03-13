import shutil
import os
import xarray as xr
import tempfile
import logging
from datapi import ApiClient
from guclimate.core import requests

logging.basicConfig(level="ERROR")


def getProducts(query=None):
    client = ApiClient()
    collections = client.get_collections(query=query)
    return collections.json["collections"]


def verify():
    client = ApiClient()
    response = client.check_authentication()
    return response


def retrieve(request: requests.CDSRequest) -> str:
    with tempfile.NamedTemporaryFile() as downloadPath:
        client = ApiClient()
        print(f"Retrieving data for request {request.params}")
        client.retrieve(request.product, target=downloadPath.name, **request.params)
        print(f"Retrieved file {downloadPath.name}")
        return downloadPath.name

        # saveResults(downloadPath.name, outputPath)


def saveResults(
    downloadPath: str,
    outputPath: str,
    format: requests.ResultFormat = requests.ResultFormat.ZIP,
):
    if format == requests.ResultFormat.ZIP:
        extractAndSave(downloadPath, outputPath)


def extractAndSave(downloadPath: str, outputPath: str):
    with tempfile.TemporaryDirectory() as tempDir:
        shutil.unpack_archive(
            downloadPath, tempDir, format=requests.ResultFormat.ZIP.value
        )

        extracted_files = [os.path.join(tempDir, file) for file in os.listdir(tempDir)]
        sorted_files = sorted(extracted_files)

        # save individual files for debugging
        # for file in sorted_files:
        #     outputDir = os.path.dirname(outputPath)
        #     fileName = os.path.basename(file)
        #     path = os.path.join(outputDir, fileName)
        #     shutil.copyfile(file, path)

        datasets = [xr.open_dataset(file, engine="cfgrib") for file in sorted_files]

        concatenated = xr.concat(datasets, dim="time")
        concatenated.to_netcdf(outputPath)
