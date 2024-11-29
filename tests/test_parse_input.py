import pytest
from src.guclimate.retrieve.parse_input import parseNumeric, createCDSRequest

numeric_inputs = [
  ("1", "01"),
  ("1, 10", ["01", "10"]),
  ("1, 2", ["01", "02"]),
  ("1-3", ["01", "02", "03"])
  ]

@pytest.mark.parametrize("test_input, expected", numeric_inputs)
def test_parse_numeric(test_input, expected):
  assert parseNumeric(test_input) == expected

request_inputs = [
    (
        {
            "product": "ecv-for-climate-change",
            "variable": "surface_air_temperature",
            "product_type": "anomaly",
            "origin": "era5",
            "climate_reference_period": "1991_2020",
            "time_aggregation": "1_month_mean",
            "year": "2022",
            "month": "01, 02",
        },
        {
            "variable": "surface_air_temperature",
            "product_type": "anomaly",
            "origin": "era5",
            "climate_reference_period": "1991_2020",
            "time_aggregation": "1_month_mean",
            "year": "2022",
            "month": ["01", "02"],
        },
    ),
    (
        {
            "product": "ecv-for-climate-change",
            "product_type": "monthly_mean",
            "variable": "precipitation",
            "origin": "era5",
            "time_aggregation": "1_month_mean",
            "year": "2024",
            "month": "1-3",
        },
        {
            "variable": "precipitation",
            "product_type": "monthly_mean",
            "origin": "era5",
            "time_aggregation": "1_month_mean",
            "year": "2024",
            "month": ["01", "02", "03"],
        },
    ),
]

@pytest.mark.parametrize("user_input, expected", request_inputs)
def test_create_cds_request(user_input, expected):
    request = createCDSRequest(user_input)
    assert request.params == expected


def test_create_cds_request_no_product():
  with pytest.raises(ValueError):
    user_input = {
      'variable': 'invalid_variable',
      'aggregation': '1_month_mean',
      'years': '2022',
      'months': '01, 02'
    }
    createCDSRequest(user_input)
