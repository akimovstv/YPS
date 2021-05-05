"""
Additional tools for checking request arguments.
"""

import datetime

INVALID_DATE_MESSAGE = 'must be valid date in format `YYYY-mm-dd` (e.g. 2020-05-05)'


def checked_date(s: str) -> str:
    """
    Return `s`, if `s` is valid date in format YYYY-mm-dd (e.g. 2021-05-05),
    otherwise raise ValueError.
    """
    return datetime.datetime.strptime(s, '%Y-%m-%d').date().isoformat()
