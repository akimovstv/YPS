"""
Additional tools for checking request arguments.
"""

import datetime


def checked_date(s: str) -> str:
    """
    Return `s`, if `s` is valid date in format YYYY-mm-dd (e.g. 2021-05-05),
    otherwise raise ValueError.
    """
    try:
        return datetime.datetime.strptime(s, '%Y-%m-%d').date().isoformat()
    except ValueError:
        raise ValueError('Must be valid date in format `YYYY-mm-dd` (e.g. 2020-05-14)')


def not_empty_name(s: str) -> str:
    """
    Return stripped `s`, if it is not empty,
    otherwise raise ValueError.
    """
    s = s.strip()
    if s:
        return s
    else:
        raise ValueError('Must contain at least one non-blank character')
