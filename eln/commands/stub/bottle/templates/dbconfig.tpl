# {{ project }}:database
import sqlite3


class Database:
    """
    Database adapter.

    Adapter to handle Sqlite database connections to store persistent data.
    """

    DEFAULT_DB_NAME = 'sqlite.db'

    def __init__(self, db_name=DEFAULT_DB_NAME, create_connection=False):
        self.__db_name = db_name
        self.__connection = None

        if create_connection:
            self.connect()

    def connect(self):
        """
        Create a database connection to the instance db.

        :return: Connection object or None
        """
        try:
            self.__connection = sqlite3.connect(self.__db_name)
        except ConnectionError as e:
            print(e)

        return self.__connection

    def get_users(self):
        self.__ensure_connection()

        cursor = self.__connection.cursor()
        cursor.execute("SELECT * FROM table_name;")

        rows = cursor.fetchall()

        for row in rows:
            print(row)

        return rows

    def save(self, value):
        self.__ensure_connection()

        cursor = self.__connection.cursor()

        raw_sql = """INSERT INTO table_name(column) VALUES (?);"""

        cursor.execute(raw_sql, (column))
        row = cursor.lastrowid

        return row

    def __ensure_connection(self):
        return self.__connection if self.__connection else self.connect()

    def __str__(self):
        return self.__db_name
