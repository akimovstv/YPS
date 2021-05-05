"""
Handlers for `/course` and `/course/<int:course_id> resources`
"""
from typing import Any, Dict, Tuple

from flask_restful import Resource, reqparse

from checkers import checked_date, not_empty_name, non_negative_int
from db import database


class ExistedCourse(Resource):
    """
    Handler for `/course/<int:course_id>`
    """
    def get(self, course_id: int):
        return f'get course with id: {course_id}'

    def patch(self, course_id: int):
        return f'patch course with id: {course_id}'

    def delete(self, course_id: int) -> Dict[str, str]:
        """
        Delete course with id `course_id` from database.
        """
        database.delete_course_by_id(course_id=course_id)
        return {'message': f'Course with id {course_id} deleted'}


class NewCourse(Resource):
    """
    Handler for `/course`
    """
    parser = reqparse.RequestParser(bundle_errors=True)
    parser.add_argument('name', location='json', type=not_empty_name, required=True)
    parser.add_argument('start', location='json', type=checked_date, required=True)
    parser.add_argument('end', location='json', type=checked_date, required=True)
    parser.add_argument('lectures', location='json', type=non_negative_int, required=True)

    def post(self) -> Tuple[Dict[str, Any], int]:
        """
        Insert a new course to database and return it as a response.
        Example:
        For `/course` with json payload {"name": "C#", "start": "2021-05-22", "end": "2022-07-31", "lectures": 23}
        newly created course returns as json:
        {
            "course_id": 12,
            "name": "C#",
            "start": "2021-05-22",
            "end": "2022-07-31",
            "lectures": 23
        }
        """
        data = self.parser.parse_args()
        created_course = dict(next(database.insert_course(
            course_name=data['name'],
            start_date=data['start'],
            end_date=data['end'],
            lectures=data['lectures']
        )))
        return created_course, 201
