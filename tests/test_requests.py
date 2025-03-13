import pytest
from guclimate.core import requests


def test_create_temperature_anomaly_request():
    request = requests.createCDSRequest(
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
        "year": ["2022"],
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
        requests.createCDSRequest(user_input)


def test_get_years():
    request = requests.createCDSRequest(
        {
            "product": "ecv-for-climate-change",
            "variable": "surface_air_temperature",
            "product_type": "anomaly",
            "origin": "era5",
            "climate_reference_period": "1991_2020",
            "time_aggregation": "1_month_mean",
            "year": "2022-2024",
            "month": "01, 02",
        }
    )
    assert request.getYears() == ["2022", "2023", "2024"]


def test_split_by_year():
    request = requests.createCDSRequest(
        {
            "product": "ecv-for-climate-change",
            "variable": "surface_air_temperature",
            "product_type": "anomaly",
            "origin": "era5",
            "climate_reference_period": "1991_2020",
            "time_aggregation": "1_month_mean",
            "year": "2022-2024",
            "month": "01, 02",
        }
    )
    requestList = request.splitByYear()
    assert len(requestList) == 3
    assert requestList[0].getYears() == ["2022"]
    assert requestList[1].getYears() == ["2023"]
    assert requestList[2].getYears() == ["2024"]


def test_get_months():
    request = requests.createCDSRequest(
        {
            "product": "ecv-for-climate-change",
            "variable": "surface_air_temperature",
            "product_type": "anomaly",
            "origin": "era5",
            "climate_reference_period": "1991_2020",
            "time_aggregation": "1_month_mean",
            "year": "2022",
            "month": "02-05",
        }
    )
    assert request.getMonths() == ["02", "03", "04", "05"]


def test_split_by_month():
    request = requests.createCDSRequest(
        {
            "product": "ecv-for-climate-change",
            "variable": "surface_air_temperature",
            "product_type": "anomaly",
            "origin": "era5",
            "climate_reference_period": "1991_2020",
            "time_aggregation": "1_month_mean",
            "year": "2022",
            "month": "02-05",
        }
    )
    requestList = request.splitByMonth()
    assert len(requestList) == 4
    assert requestList[0].getMonths() == ["02"]
    assert requestList[1].getMonths() == ["03"]
    assert requestList[2].getMonths() == ["04"]
    assert requestList[3].getMonths() == ["05"]


def test_split_by_day():
    request = requests.createCDSRequest(
        {
            "product": "ecv-for-climate-change",
            "variable": "surface_air_temperature",
            "product_type": "anomaly",
            "origin": "era5",
            "climate_reference_period": "1991_2020",
            "time_aggregation": "1_month_mean",
            "year": "2022",
            "month": "02",
            "day": "01-05",
        }
    )
    requestList = request.splitByDay()
    assert len(requestList) == 5
    assert requestList[0].getDays() == ["01"]
    assert requestList[1].getDays() == ["02"]
    assert requestList[2].getDays() == ["03"]
    assert requestList[3].getDays() == ["04"]
    assert requestList[4].getDays() == ["05"]
