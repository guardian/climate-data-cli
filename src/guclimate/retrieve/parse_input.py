from datetime import time
import re

#################
# INTEGER INPUT #
#################


def parseNumeric(input: str | int):
    if isinstance(input, int):
        return [str(input).zfill(2)]

    stripped = input.strip()
    value = parseInteger(stripped)
    if value:
        return [value]

    value = parseRange(stripped)
    if value:
        return value

    value = parseCommaSeparatedIntegers(stripped)
    if value:
        return value

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


######################
# TIME INPUT (HH:MM) #
######################


def parseTime(input: str):
    # Match single time
    pattern = re.compile(r"^[0-9]{2}:[0-9]{2}$")
    if pattern.match(input) is not None:
        return [input]

    # Match comma separated times
    commaSeparated = parseCommaSeparatedTimes(input)
    if commaSeparated is not None:
        return commaSeparated

    # Match time range
    range = parseTimeRange(input)
    if range is not None:
        return range

    raise ValueError(f"Unable to parse time input: {input}")


def parseCommaSeparatedTimes(input: str):
    pattern = re.compile(r"^[0-9]{2}:[0-9]{2},\s?[0-9]{2}:[0-9]{2}$")
    if pattern.match(input) is None:
        return None

    components = input.split(",")
    return [time.strip() for time in components]


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
