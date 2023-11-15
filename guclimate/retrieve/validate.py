from inquirer import errors
from collections.abc import Callable
import re


def isInteger(_, current):
    try:
        int(current)
    except ValueError:
        raise errors.ValidationError("", reason="Please enter an integer value")

    return True


def isMonthRange(_, current):
    stripped = current.strip()
    error = errors.ValidationError("", reason=f"{current} is not a valid month range")

    pattern = re.compile("^[0-9]{1,2}-[0-9]{1,2}$")
    if pattern.match(stripped) is None:
        raise error

    [first, last] = [int(value) for value in stripped.split("-")]
    # check that values are between 1 and 12
    if first < 1 or first > 12 or last < 1 or last > 12:
        raise error

    # check that last is greater than first
    if last <= first:
        raise error

    return True


def isYearRange(_, current):
    stripped = current.strip()
    error = errors.ValidationError("", reason=f"{current} is not a valid year range")

    pattern = re.compile("^[0-9]{4}-[0-9]{4}$")
    if pattern.match(stripped) is None:
        raise error

    [first, last] = [int(value) for value in stripped.split("-")]

    # check that last is greater than first
    if last <= first:
        raise error

    return True


def isCommaSeparatedIntegers(_, current):
    components = current.split(",")
    numbers = [c.strip() for c in components]
    for number in numbers:
        try:
            int(number)
        except ValueError:
            raise errors.ValidationError(
                "Comma-separated should only contain integer values"
            )

    return True


def combineOR(validators: list[Callable], reason: str):
    def validate(answers, current):
        for validator in validators:
            try:
                validator(answers, current)
                return True
            except errors.ValidationError:
                pass

        raise errors.ValidationError("", reason=reason)

    return validate
