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

    def __init__(self, variable: str):
        self.variable = variable

    def params(self) -> dict:
        return {
            "variable": self.variable,
            "product_type": "anomaly",
            "climate_reference_period": "1991_2020",
            "time_aggregation": "1_month_mean",
            "year": [
                "2022",
                "2021",
            ],
            "month": "10",
            "origin": "era5",
            "format": self.format.value,
        }
    
