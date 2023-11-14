import inquirer
from collections.abc import Callable
import re


def isInteger(_, current):
    try:
        int(current)
    except ValueError:
        raise inquirer.errors.ValidationError(
            "", reason="Please enter an integer value"
        )

    return True


def isMonthRange(_, current):
    pattern = re.compile("^[0-9]{1,2}-[0-9]{1,2}$")
    if pattern.match(current.strip()):
        return True
    else:
        raise inquirer.errors.ValidationError(
            "", reason=f"{current} is not a valid month range"
        )


def isCommaSeparatedIntegers(_, current):
    components = current.split(",")
    numbers = [c.strip() for c in components]
    for number in numbers:
        try:
            int(number)
        except ValueError:
            raise inquirer.errors.ValidationError(
                "Comma-separated should only contain integer values"
            )

    return True


def combineOR(validators: list[Callable], reason: str):
    def validate(answers, current):
        for validator in validators:
            try:
                validator(answers, current)
                return True
            except inquirer.errors.ValidationError:
                pass

        raise inquirer.errors.ValidationError("", reason=reason)


    return validate
