import re

from voluptuous import (All, Length)
from voluptuous.error import ValueInvalid
from voluptuous.schema_builder import message


@message('expected an Temperature', cls=ValueInvalid)
def Temperature(v):
    TEMPERATURE_REGEX = re.compile(
        r'^[-+]?\d{1,10}(\.\d*)?[CFK]?$',  # work with float
        re.IGNORECASE
    )

    if not (TEMPERATURE_REGEX.match(v)):
        raise ValueInvalid('Invalid temperature {}'.format(v))
    return v


temperature_validator = All(Temperature(), Length(max=20))
