from datetime import timedelta
from enum import Enum, auto
from typing import Union


class Infinity(Enum):
    """Represent positive and negative infinity."""

    POSITIVE = auto()  # noqa: WPS115


# The approach is borrowed from https://github.com/python/typing/issues/236
# I decided to more explicit about representing the Infinity value and not
# resort to ... or None.
Timeout = Union[Infinity, timedelta]
