import pytest
from src.guclimate.retrieve.parse_input import parseNumeric, createCDSRequest

numeric_inputs = [
    ("1", "01"),
    ("1, 10", ["01", "10"]),
    ("1, 2", ["01", "02"]),
    ("1-3", ["01", "02", "03"]),
]


@pytest.mark.parametrize("test_input, expected", numeric_inputs)
def test_parse_numeric(test_input, expected):
    assert parseNumeric(test_input) == expected


def test_create_temperature_anomaly_request():
    request = createCDSRequest(
        {
            "product": "ecv-for-climate-change",
            "variable": "surface_air_temperature",
            "product_type": "anomaly",
            "origin": "era5",
            "climate_reference_period": "1991_2020",
            "time_aggregation": "1_month_mean",
            "year": "2022",
            "month": "01, 02",
        }
    )
    assert request.params == {
        "variable": "surface_air_temperature",
        "product_type": "anomaly",
        "origin": "era5",
        "climate_reference_period": "1991_2020",
        "time_aggregation": "1_month_mean",
        "year": "2022",
        "month": ["01", "02"],
    }


def test_create_cds_request_no_product():
    with pytest.raises(ValueError):
        user_input = {
            "variable": "invalid_variable",
            "aggregation": "1_month_mean",
            "years": "2022",
            "months": "01, 02",
        }
        createCDSRequest(user_input)
