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


class AnomalyRequest:
    product = "ecv-for-climate-change"
    format = ResultFormat.ZIP

    def __init__(
        self,
        productType: str,
        variable: str,
        timeAggregation="1_month_mean",
        years="",
        months="",
    ):
        self.productType = productType
        self.variable = variable
        self.timeAggregation = timeAggregation
        self.years = years
        self.months = months

    def params(self) -> dict:
        return {
            "variable": self.variable,
            "product_type": self.productType,
            "climate_reference_period": "1991_2020",
            "time_aggregation": self.timeAggregation,
            "year": self.years,
            "month": self.months,
            "origin": "era5",
            "format": self.format.value,
        }
