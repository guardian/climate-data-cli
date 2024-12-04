import cdsapi
import shutil
import os
import xarray as xr
import tempfile
import logging
from datapi import ApiClient
from guclimate.core import requests

logging.basicConfig(level="ERROR")

products = {
    "Essential Climate Variables (ECV) for climate change": "ecv-for-climate-change",
    "ERA5 reanalysis (single levels)": "reanalysis-era5-single-levels",
}

def getProducts():
    client = ApiClient()
    collections = client.get_collections()
    return collections.json["collections"]

def verify():
    client = ApiClient()
    response = client.check_authentication()
    return response

def retrieve(request: requests.CDSRequest, outputPath: str) -> cdsapi.api.Result:
    with tempfile.NamedTemporaryFile() as downloadPath:
        client = cdsapi.Client()
        client.retrieve(
            request.product,
            request.params,
            downloadPath.name,
        )

        saveResults(downloadPath.name, outputPath)


def saveResults(
    downloadPath: str, outputPath: str, format: requests.ResultFormat = requests.ResultFormat.ZIP
):
    if format == requests.ResultFormat.ZIP:
        extractAndSave(downloadPath, outputPath)


def extractAndSave(downloadPath: str, outputPath: str):
    with tempfile.TemporaryDirectory() as tempDir:
        shutil.unpack_archive(downloadPath, tempDir, format=requests.ResultFormat.ZIP.value)

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
