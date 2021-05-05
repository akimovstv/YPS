"""
Handler for `/catalogue`
"""

from typing import Any, Dict, List

from flask_restful import Resource, reqparse

from checkers import checked_date, not_empty_name
from db import database


class Catalogue(Resource):
    """
    Handler for `/catalogue`
    """
    parser = reqparse.RequestParser(bundle_errors=True)
    parser.add_argument('course-name', location='args', type=not_empty_name)
    parser.add_argument('start-date-after', location='args', type=checked_date)
    parser.add_argument('end-date-before', location='args', type=checked_date)

    def get(self) -> List[Dict[str, Any]]:
        """
        Return list of courses, applying filtering if parameters provided in the URL.
        Examples:
        1) For `/catalogue` return all courses in the catalogue.
        2) For `/catalogue?course-name=Pro Python` return only courses that have the name 'Pro Python'
        3) For `/catalogue?course-name=Go&start-date-after=2020-11-12` return only courses that have the name 'Go'
           and start after or exactly on 2020-11-12.
        4) For `/catalogue?course-name=C&start-date-after=2020-11-12&end-date-before=2020-11-30` return only courses
           that have the name `C` and start and finish in period from 2020-11-12 and 2020-11-30.
        etc.
        """
        args = self.parser.parse_args()
        courses = list(map(dict, database.get_courses(
            name=args['course-name'],
            start_date_after=args['start-date-after'],
            end_date_before=args['end-date-before']
        )))
        return courses
