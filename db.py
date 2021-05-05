from sqlite3 import connect, Row
from typing import Iterator, Optional


class Database:
    def __init__(self, path: str) -> None:
        self._path = path

    def create_tables(self) -> None:
        with connect(self._path) as connection:
            connection.execute("""
                CREATE TABLE IF NOT EXISTS courses
                (
                    CourseID    INTEGER PRIMARY KEY AUTOINCREMENT,
                    Name        TEXT    NOT NULL,
                    StartDate   TEXT    NOT NULL,
                    EndDate     TEXT    NOT NULL,
                    NumLectures INTEGER NOT NULL
                )
            """)

    def get_courses(
            self,
            *,
            name: Optional[str] = None,
            start_date_after: Optional[str] = None,
            end_date_before: Optional[str] = None
    ) -> Iterator[Row]:
        """
        Select courses from database applying filtering by `name`, `start_date_after`, `end_date_before` if any.
        """
        with connect(self._path) as connection:
            connection.row_factory = Row
            query = """
                SELECT
                    CourseID    AS course_id,
                    Name        AS name,
                    StartDate   AS start,
                    EndDate     AS end,
                    NumLectures AS lectures
                FROM
                    courses
            """

            if name and start_date_after and end_date_before:
                query += """
                    WHERE
                          Name = ?
                      AND DATE(StartDate) >= DATE(?)
                      AND DATE(EndDate) <= DATE(?)
                """
                parameters = (name, start_date_after, end_date_before)
            elif name and start_date_after:
                query += """
                    WHERE
                          Name = ?
                      AND DATE(StartDate) >= DATE(?)
                """
                parameters = (name, start_date_after)
            elif name and end_date_before:
                query += """
                    WHERE
                          Name = ?
                      AND DATE(EndDate) <= DATE(?)
                """
                parameters = (name, end_date_before)
            elif name:
                query += """
                    WHERE
                          Name = ?
                """
                parameters = (name,)
            elif start_date_after and end_date_before:
                query += """
                    WHERE
                          DATE(StartDate) >= DATE(?)
                      AND DATE(EndDate) <= DATE(?)
                """
                parameters = (start_date_after, end_date_before)
            elif start_date_after:
                query += """
                    WHERE
                          DATE(StartDate) >= DATE(?)
                """
                parameters = (start_date_after,)
            elif end_date_before:
                query += """
                    WHERE
                          DATE(EndDate) <= DATE(?)
                """
                parameters = (end_date_before,)
            else:
                parameters = ()

            for row in connection.execute(query, parameters):
                yield row

    def insert_course(
            self,
            *,
            course_name: str,
            start_date: str,
            end_date: str,
            lectures: int
    ) -> Iterator[Row]:
        with connect(self._path) as connection:
            cursor = connection.cursor()
            cursor.execute(
                """
                INSERT INTO
                    courses (Name, StartDate, EndDate, NumLectures)
                VALUES
                    (?, ?, ?, ?)
                """,
                (course_name, start_date, end_date, lectures)
            )
            return self.get_course_by_id(course_id=cursor.lastrowid)

    def get_course_by_id(
            self,
            *,
            course_id: int
    ) -> Iterator[Row]:
        with connect(self._path) as connection:
            connection.row_factory = Row
            for row in connection.execute(
                    """
                    SELECT
                        CourseID    AS course_id,
                        Name        AS name,
                        StartDate   AS start,
                        EndDate     AS end,
                        NumLectures AS lectures
                    FROM
                        courses
                    WHERE
                        CourseID = ?;                
                    """,
                    (course_id,)
            ):
                yield row

    def change_course_by_id(
            self,
            *,
            course_id: int,
            course_name: str,
            start_date: str,
            end_date: str,
            lectures: int
    ):
        with connect(self._path) as connection:
            connection.execute(
                """
                UPDATE courses
                SET
                    Name=?,
                    StartDate=?,
                    EndDate=?,
                    NumLectures=?
                WHERE
                    CourseID = ?
                """,
                (course_name, start_date, end_date, lectures, course_id)
            )

    def delete_course_by_id(
            self,
            *,
            course_id: int
    ) -> None:
        with connect(self._path) as connection:
            connection.execute(
                """DELETE FROM courses WHERE CourseID = ?""",
                (course_id,)
            )


database = Database('data.db')
