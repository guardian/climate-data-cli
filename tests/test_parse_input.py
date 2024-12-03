import pytest
from src.guclimate.retrieve.parse_input import parseNumeric, parseTime, createCDSRequest

numeric_inputs = [
    ("1", "01"),
    ("1, 10", ["01", "10"]),
    ("1, 2", ["01", "02"]),
    ("1-3", ["01", "02", "03"]),
]

@pytest.mark.parametrize("test_input, expected", numeric_inputs)
def test_parse_numeric(test_input, expected):
    assert parseNumeric(test_input) == expected


time_inputs = [
    ("00:00", ["00:00"]),
    ("00:00, 02:00", ["00:00", "02:00"]),
    ("00:00-02:00", ["00:00", "01:00", "02:00"]),
    ("00:00-23:00", [
        "00:00", "01:00", "02:00",
        "03:00", "04:00", "05:00",
        "06:00", "07:00", "08:00",
        "09:00", "10:00", "11:00",
        "12:00", "13:00", "14:00",
        "15:00", "16:00", "17:00",
        "18:00", "19:00", "20:00",
        "21:00", "22:00", "23:00"
    ]),
]

@pytest.mark.parametrize("test_input, expected", time_inputs)
def test_parse_time(test_input, expected):
    assert parseTime(test_input) == expected


def test_start_time_must_be_before_end_time():
    with pytest.raises(ValueError):
        parseTime("23:00-08:00")


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
