from typing import Protocol

class CDSRequest(Protocol):
    """Definition for request from Climate Data Store (CDS)"""
    product: str

    def params(self) -> dict:
         """Request parameters"""

class AnomalyRequest:
    product = "ecv-for-climate-change"

    def __init__(self, variable: str):
        self.variable = variable

    def params(self) -> dict:
        return {
            "variable": self.variable,
            "product_type": "anomaly",
            "climate_reference_period": "1991_2020",
            "time_aggregation": "1_month_mean",
            "year": [
                "1940",
                "1941",
            ],
            "month": [
                "01",
                "02",
            ],
            "origin": "era5",
            "format": "zip",
        }