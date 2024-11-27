import cdsapi
import shutil
import os
import xarray as xr
import tempfile
from guclimate.retrieve import requests

ResultFormat = requests.ResultFormat

def retrieve(request: requests.CDSRequest, outputPath: str) -> cdsapi.api.Result:
    with tempfile.NamedTemporaryFile() as downloadPath:
        client = cdsapi.Client()
        client.retrieve(
            request.product,
            request.params(),
            downloadPath.name,
        )

        saveResults(downloadPath.name, outputPath)


def saveResults(
    downloadPath: str, outputPath: str, format: ResultFormat = ResultFormat.ZIP
):
    if format == requests.ResultFormat.ZIP:
        extractAndSave(downloadPath, outputPath)


def extractAndSave(downloadPath: str, outputPath: str):
    with tempfile.TemporaryDirectory() as tempDir:
        shutil.unpack_archive(downloadPath, tempDir, format=ResultFormat.ZIP.value)

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
