from guclimate.retrieve.requests import CDSRequest, ResultFormat
import re

numericKeys = ["year", "years", "month", "months"]

def createCDSRequest(config: dict) -> CDSRequest:
    if "product" not in config:
        raise ValueError("Missing product for request")

    product = config["product"]
    numericParams = {key: parseNumeric(config[key]) for key in numericKeys if key in config}
    otherParams = {key: config[key] for key in config if key not in numericKeys and key not in ["product"]}
    params = numericParams | otherParams
    return CDSRequest(product, params)

def parseNumeric(input: str):
    stripped = input.strip()
    month = parseInteger(stripped)
    if month:
        return month

    months = parseRange(stripped)
    if months:
        return months

    months = parseCommaSeparatedIntegers(stripped)
    if months:
        return months

    raise ValueError(f"Unable to parse input: {input}")


def parseInteger(input: str):
    try:
        return str(int(input)).zfill(2)
    except ValueError:
        return None


def parseRange(input: str):
    pattern = re.compile("^[0-9]{1,4}-[0-9]{1,4}$")
    if pattern.match(input) is None:
        return None

    [first, last] = [int(value) for value in input.split("-")]
    months = range(first, last + 1)
    return [str(month).zfill(2) for month in months]


def parseCommaSeparatedIntegers(input: str):
    components = input.split(",")
    months = [int(c) for c in components]
    return [str(month).zfill(2) for month in months]
