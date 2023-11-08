import cdsapi
import shutil
import os
import time
from guclimate import cache, requests

client = cdsapi.Client(quiet=True)

def retrieve(request: requests.CDSRequest) -> cdsapi.api.Result:
    path = cache.uniqueFilePath()

    client = cdsapi.Client()
    client.retrieve(
        request.product,
        request.params(),
        f"{path}.{request.format.value}",
    )

    return ResultSet(path, request.format)

class ResultSet:
    def __init__(self, path, format: requests.ResultFormat) -> None:
        fullPath = f"{path}.{format.value}"

        if format == requests.ResultFormat.ZIP:
            shutil.unpack_archive(fullPath, path)

        self.files = [f for f in os.listdir(path)]


