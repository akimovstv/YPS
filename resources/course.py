from flask_restful import Resource


class ExistedCourse(Resource):
    """
    Resource that works with /course/<int:course_id>
    """

    def get(self, course_id: int):
        return f'get course with id: {course_id}'

    def patch(self, course_id: int):
        return f'patch course with id: {course_id}'

    def delete(self, course_id: int):
        return f'delete course with id: {course_id}'


class NewCourse(Resource):
    """
    Resource that works with /course
    """
    def post(self):
        return 'post new course'