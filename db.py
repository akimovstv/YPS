from sqlite3 import connect, Row
from typing import Iterator, Optional


class Database:
    def __init__(self, path: str) -> None:
        self._path = path
        self.create_tables()

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
            start_date: Optional[str] = None,
            end_date: Optional[str] = None
    ) -> Iterator[Row]:
        """
        Select courses from database applying filtering by `name`, `start_date`, `end_date` if any.
        """
        with connect(self._path) as connection:
            connection.row_factory = Row
            query = """
                SELECT
                    CourseID    AS course_id,
                    Name        AS name,
                    StartDate   AS start,
                    EndDate     AS end,
                    NumLectures AS num_lectures
                FROM
                    courses
            """

            if name and start_date and end_date:
                query += """
                    WHERE
                          Name = ?
                      AND DATE(StartDate) <= DATE(?)
                      AND DATE(EndDate) >= DATE(?)
                """
                parameters = (name, start_date, end_date)
            elif name and start_date:
                query += """
                    WHERE
                          Name = ?
                      AND DATE(StartDate) <= DATE(?)
                """
                parameters = (name, start_date)
            elif name and end_date:
                query += """
                    WHERE
                          Name = ?
                      AND DATE(EndDate) >= DATE(?)
                """
                parameters = (name, end_date)
            elif name:
                query += """
                    WHERE
                          Name = ?
                """
                parameters = (name,)
            elif start_date and end_date:
                query += """
                    WHERE
                          DATE(StartDate) <= DATE(?)
                      AND DATE(EndDate) >= DATE(?)
                """
                parameters = (start_date, end_date)
            elif start_date:
                query += """
                    WHERE
                          DATE(StartDate) <= DATE(?)
                """
                parameters = (start_date,)
            elif end_date:
                query += """
                    WHERE
                          DATE(EndDate) >= DATE(?)
                """
                parameters = (end_date,)
            else:
                parameters = ()

            for row in connection.execute(query, parameters):
                yield row


if __name__ == '__main__':
    db = Database('first.db')
    import pprint

    pprint.pprint(
        list(map(dict, db.get_courses(
            start_date='2019-01-01',
            end_date='2019-01-23'
        )))
    )
