"""
Handlers for `/course` and `/course/<int:course_id> resources`
"""
from typing import Any, Dict, Tuple, Union

from flask_restful import Resource, reqparse

from checkers import checked_date, not_empty_name, non_negative_int
from db import database


class ExistedCourse(Resource):
    """
    Handler for `/course/<int:course_id>`
    """
    parser = reqparse.RequestParser(bundle_errors=True)
    parser.add_argument('name', location='json', type=not_empty_name)
    parser.add_argument('start', location='json', type=checked_date)
    parser.add_argument('end', location='json', type=checked_date)
    parser.add_argument('lectures', location='json', type=non_negative_int)

    def get(self, course_id: int) -> Union[Dict, Tuple[Dict, int]]:
        """
        Return course with provided `course_id`.
        """
        try:
            course = dict(next(database.get_course_by_id(course_id=course_id)))
            return course
        except StopIteration:
            return {'message': f'Course with id {course_id} not found'}, 404

    def patch(self, course_id: int) -> Union[Dict, Tuple[Dict, int]]:
        """
        Update fields in course with `course_id` with optional values from payload.
        """
        data = self.parser.parse_args()
        try:
            course = dict(next(database.get_course_by_id(course_id=course_id)))
            database.change_course_by_id(
                course_id=course_id,
                course_name=data['name'] or course['name'],
                start_date=data['start'] or course['start'],
                end_date=data['end'] or course['end'],
                lectures=data['lectures'] or course['lectures']
            )
            return {'message': f'Course with id {course_id} updated'}
        except StopIteration:
            return {'message': f'Course with id {course_id} not found'}, 404

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
