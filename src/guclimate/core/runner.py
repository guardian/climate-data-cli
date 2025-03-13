from guclimate.core.recipe import Recipe
from guclimate.core import requests
from guclimate.retrieve import cds
from datapi import ApiClient
from pathlib import Path


class Runner:
    def __init__(self, recipe: Recipe):
        self.recipe = recipe

    def run(self):
        self.retrieveData()

    def retrieveData(self):
        retrievals = self.recipe.retrievals()
        for retrieval in retrievals:
            self.runRetrieval(retrieval)

    def runRetrieval(self, retrieval):
        print("----------------------------")
        print(f"Retrieving '{retrieval.key}'")

        path = retrieval.outputPath
        if Path(path).is_file():
            print(f"Output file exists: {path}")
            print("----------------------------")
            return

        request = requests.createCDSRequest(retrieval.params)
        requestList = self.splitRequestIfNeeded(request)
        print(f"Number of requests: {len(requestList)}")

        files = [cds.retrieve(request) for request in requestList]
        for file in files:
            print(f"Retrieved file: {file}")

    def shouldSplitRequest(self, request):
        client = ApiClient()
        estimate = client.estimate_costs(request.product, **request.params)

        shouldSplit = estimate["cost"] > estimate["limit"]
        if shouldSplit:
            print(f"Splitting request... {estimate}")

        return shouldSplit

    def splitRequestIfNeeded(self, request):
        if self.shouldSplitRequest(request):
            # split by year
            return request.splitByYear()
        else:
            return [request]
