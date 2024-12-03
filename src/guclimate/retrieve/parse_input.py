from guclimate.retrieve.requests import CDSRequest
from datetime import time
import re

numericKeys = ["year", "years", "month", "months", "day", "days"]

def createCDSRequest(config: dict) -> CDSRequest:
    if "product" not in config:
        raise ValueError("Missing product for request")

    product = config["product"]
    params = {}

    # Parse time param
    time = config.get("time", None)
    if time is not None:
        params["time"] = parseTime(time)
    print(params)

    # Parse numeric params, i.e. day, month, year
    numericParams = {key: parseNumeric(config[key]) for key in numericKeys if key in config}
    params |= numericParams
    print(params)

    otherParams = {key: config[key] for key in config if key not in numericKeys and key not in ["product", "output"]}
    params = numericParams | otherParams
    return CDSRequest(product, params)

def parseTime(input: str):
    print(f"parse time {input}")
    ## Match single time
    pattern = re.compile("^[0-9]{2}:[0-9]{2}$")
    if pattern.match(input) is not None:
        return [input]

    ## Match comma separated times
    pattern = re.compile(r"^[0-9]{2}:[0-9]{2},\s?[0-9]{2}:[0-9]{2}$")
    if pattern.match(input) is not None:
        components = input.split(",")
        return [time.strip() for time in components]

    ## Match time range
    range = parseTimeRange(input)
    if range is not None:
        return range

    raise ValueError(f"Unable to parse time input: {input}")


def parseTimeRange(input: str):
    pattern = re.compile(r"^[0-9]{2}:[0-9]{2}\s?-\s?[0-9]{2}:[0-9]{2}$")
    if pattern.match(input) is None:
        return None

    [start, end] = input.split("-")
    start_time = time.fromisoformat(start)
    end_time = time.fromisoformat(end)

    if start_time > end_time:
        raise ValueError("Start time must be before end time")

    range = []
    current_time = start_time
    while current_time <= end_time:
        range.append(current_time.isoformat(timespec="minutes"))
        if current_time.hour < 23:
            current_time = current_time.replace(hour=current_time.hour + 1)
        else:
            break

    return range

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
    pattern = re.compile(r"^[0-9]{1,4}-[0-9]{1,4}$")
    if pattern.match(input) is None:
        return None

    [first, last] = [int(value) for value in input.split("-")]
    months = range(first, last + 1)
    return [str(month).zfill(2) for month in months]


def parseCommaSeparatedIntegers(input: str):
    components = input.split(",")
    months = [int(c) for c in components]
    return [str(month).zfill(2) for month in months]
