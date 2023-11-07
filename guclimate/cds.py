import cdsapi
import guclimate.requests as requests

client = cdsapi.Client()

def retrieve(request: requests.CDSRequest):
    client = cdsapi.Client()
    client.retrieve(
        request.product,
        request.params(),
        "download.zip",
    )
