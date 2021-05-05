import sqlite3


class Database:
    def __init__(self, path: str) -> None:
        self._path = path
        self.create_tables()

    def create_tables(self):
        with sqlite3.connect(self._path) as connection:
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

    def get_all_courses(self):
        with sqlite3.connect(self._path) as connection:
            for row in connection.execute("""
                SELECT
                    CourseID    AS course_id,
                    Name        AS name,
                    StartDate   AS start,
                    EndDate     AS end,
                    NumLectures AS num_lectures
                FROM
                    courses
            """):
                yield row


if __name__ == '__main__':
    db = Database('first.db')
    print(list(db.get_all_courses()))
