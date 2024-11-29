from enum import Enum

class ResultFormat(str, Enum):
    ZIP = "zip"

class CDSRequest:
    """Definition for request from Climate Data Store (CDS)"""
    product: str
    params: dict

    def __init__(self, product: str, params: dict):
        self.product = product
        self.params = params

    def format(self) -> ResultFormat:
        if "format" not in self.params:
            return
        return ResultFormat(self.params["format"])
