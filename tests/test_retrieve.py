import pytest
from src.guclimate.retrieve.parse_input import parseNumeric, createECVRequest

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
  ("anomaly", 
  {
    'variable': 'surface_air_temperature', 
    'aggregation': '1_month_mean', 
    'years': '2022', 
    'months': '01, 02'
  }, 
  {
    'variable': 'surface_air_temperature',
    'product_type': 'anomaly',
    'origin': 'era5',
    'climate_reference_period': '1991_2020', 
    'time_aggregation': '1_month_mean',
    'year': '2022',
    'month': ['01', '02'], 
  }),
  ("monthly_mean",
  {
    'variable': 'precipitation', 
    'aggregation': '1_month_mean',
    'years': '2024',
    'months': '1-3'
  },
  {
    'variable': 'precipitation',
    'product_type': 'monthly_mean',
    'origin': 'era5',
    'time_aggregation': '1_month_mean',
    'year': '2024',
    'month': ['01', '02', '03'], 
  })
]

@pytest.mark.parametrize("product_type, user_input, expected", request_inputs)
def test_create_ecv_request(product_type, user_input, expected):
  request = createECVRequest(product_type, user_input)
  assert request.params() == expected
