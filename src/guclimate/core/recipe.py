class Recipe:
    def __init__(self, yaml: str):
        self.yaml = yaml

    def retrievals(self):
        retrievals = self.yaml["retrieve"]
        return [Retrieval(key, retrievals[key]) for key in retrievals]


class Retrieval:
    key: str
    params: dict
    outputPath: str

    def __init__(self, key: str, params: dict):
        self.key = key
        self.params = params
        self.outputPath = params["output"]
