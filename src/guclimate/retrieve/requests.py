from typing import Protocol
from enum import Enum


class ResultFormat(str, Enum):
    ZIP = "zip"


class CDSRequest(Protocol):
    """Definition for request from Climate Data Store (CDS)"""

    product: str
    format: ResultFormat

    def params(self) -> dict:
        """Request parameters"""


class ECVRequest:
    product = "ecv-for-climate-change"
    format = ResultFormat.ZIP

    def __init__(
        self,
        productType: str,
        variable: str,
        origin="era5",
        climateReferencePeriod="1991_2020",
        timeAggregation="1_month_mean",
        years="",
        months="",
    ):
        self.productType = productType
        self.variable = variable
        self.origin = origin
        self.climateReferencePeriod = climateReferencePeriod
        self.timeAggregation = timeAggregation
        self.years = years
        self.months = months

    def params(self) -> dict:
        params = {
            "variable": self.variable,
            "product_type": self.productType,
            "time_aggregation": self.timeAggregation,
            "year": self.years,
            "month": self.months,
            "origin": self.origin,
        }

        if self.productType == "anomaly":
            params["climate_reference_period"] = self.climateReferencePeriod

        return params
