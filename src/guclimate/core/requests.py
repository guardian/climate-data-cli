from enum import Enum
from functools import reduce
from typing import List, Self
from guclimate.retrieve.parse_input import parseNumeric, parseTime

NUMERIC_PARAMS = ["year", "years", "month", "months", "day", "days"]


class ResultFormat(str, Enum):
    ZIP = "zip"


class CDSRequest:
    """Definition for request from Climate Data Store (CDS)"""

    product: str
    params: dict

    def __init__(self, product: str, params: dict):
        self.product = product
        self.params = params

    def copy(self):
        return CDSRequest(self.product, self.params.copy())

    def format(self) -> ResultFormat:
        if "format" not in self.params:
            return
        return ResultFormat(self.params["format"])

    def getYears(self) -> List[str]:
        return self.params.get("year", [])

    def setYears(self, years: List[str]):
        self.params["year"] = years

    def splitByYear(self) -> List[Self]:
        years = self.getYears()
        if len(years) <= 1:
            return [self]
        else:
            requests = []
            for year in years:
                request = self.copy()
                request.setYears([year])
                requests.append(request)
            return requests

    def getMonths(self) -> List[str]:
        return self.params.get("month", [])

    def setMonths(self, months: List[str]):
        self.params["month"] = months

    def splitByMonth(self) -> List[Self]:
        months = self.getMonths()
        if len(months) <= 1:
            return [self]
        else:
            requests = []
            for month in months:
                request = self.copy()
                request.setMonths([month])
                requests.append(request)
            return requests

    def getDays(self) -> List[str]:
        return self.params.get("day", [])

    def setDays(self, days: List[str]):
        self.params["day"] = days

    def splitByDay(self) -> List[Self]:
        days = self.getDays()
        if len(days) <= 1:
            return [self]
        else:
            requests = []
            for day in days:
                request = self.copy()
                request.setDays([day])
                requests.append(request)
            return requests


def createCDSRequest(config: dict) -> CDSRequest:
    if "product" not in config:
        raise ValueError("Missing product for request")

    product = config["product"]

    def parseParams(acc, key):
        # exclude product and output from request params
        if key in ["product", "output"]:
            return acc

        if key in NUMERIC_PARAMS:
            acc[key] = parseNumeric(config[key])
        elif key == "time":
            acc[key] = parseTime(config[key])
        else:
            acc[key] = config[key]

        return acc

    params = reduce(parseParams, config, {})
    return CDSRequest(product, params)
