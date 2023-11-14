import cdsapi
import shutil
import os
import xarray as xr
import xcdat
from guclimate import cache, requests

client = cdsapi.Client(quiet=True)


def retrieve(request: requests.CDSRequest) -> cdsapi.api.Result:
    cacheDirectory = cache.cacheDirectory()
    filename = cache.uniqueFilename()
    targetPath = os.path.join(cacheDirectory, f"{filename}.{request.format.value}")

    client = cdsapi.Client()
    client.retrieve(
        request.product,
        request.params(),
        targetPath,
    )

    return ResultSet(cacheDirectory, filename, request.format)


class ResultSet:
    files = []

    def __init__(self, targetDir, filename, format: requests.ResultFormat) -> None:
        filepath = os.path.join(targetDir, f"{filename}.{format.value}")

        if format == requests.ResultFormat.ZIP:
            extract_dir = os.path.join(targetDir, filename)
            shutil.unpack_archive(filepath, extract_dir)
            extracted_files = [os.path.join(extract_dir, f) for f in os.listdir(extract_dir)]
            self.files = sorted(extracted_files)

    def save(self, path):
        datasets = [xcdat.open_dataset(file, engine="cfgrib") for file in self.files]
        concatenated = xr.concat(datasets, dim="time")
        concatenated.to_netcdf(path)
