"""
Additional tools for checking request arguments.
"""

import datetime

INVALID_DATE_MESSAGE = 'must be valid date in format `YYYY-mm-dd` (e.g. 2020-05-05)'
INVALID_NAME_MESSAGE = 'must contain at least one non-blank character'


def checked_date(s: str) -> str:
    """
    Return `s`, if `s` is valid date in format YYYY-mm-dd (e.g. 2021-05-05),
    otherwise raise ValueError.
    """
    return datetime.datetime.strptime(s, '%Y-%m-%d').date().isoformat()


def not_empty_name(s: str) -> str:
    """
    Return stripped `s`, if it is not empty,
    otherwise raise ValueError.
    """
    s = s.strip()
    if s:
        return s
    else:
        raise ValueError
