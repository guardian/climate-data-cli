from guclimate import requests
from guclimate import validate
import re


def createAnomalyRequest(input: dict) -> requests.AnomalyRequest:
    variable = input["variable"]
    months = parseMonths(input["months"])
    return requests.AnomalyRequest(variable, months=months)


def parseMonths(input: str):
    stripped = input.strip()
    month = parseInteger(stripped)
    if month:
        return month

    months = parseMonthRange(stripped)
    if months:
        return months
    
    months = parseCommaSeparatedIntegers(stripped)
    if months:
        return months

    raise ValueError("Cannot create request without month parameter")


def parseInteger(input: str):
    try:
        return str(int(input)).zfill(2)
    except ValueError:
        return None


def parseMonthRange(input: str):
    pattern = re.compile("^[0-9]{1,2}-[0-9]{1,2}$")
    if pattern.match(input) is None:
        return None

    [first, last] = [int(value) for value in input.split("-")]
    months = range(first, last + 1)
    return [str(month).zfill(2) for month in months]


def parseCommaSeparatedIntegers(input: str):
    components = input.split(",")
    months = [int(c) for c in components]
    return [str(month).zfill(2) for month in months]
