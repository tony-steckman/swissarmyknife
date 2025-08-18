"""src/lib/sqlite.py
A simple SQLite database interface for Python developers.
This module provides basic functionality to connect to a SQLite database,
execute queries, and manage data.
"""

import sqlite3


class Database:
    """A simple SQLite database interface."""

    def __init__(self, db_path):
        self.db_path = db_path
        self.connection = None

    def connect(self):
        """Establish a connection to the SQLite database.
        If the connection already exists, it will be reused.
        """
        self.connection = sqlite3.connect(self.db_path)

    def close(self):
        """Close the database connection if it exists."""
        if self.connection:
            self.connection.close()
            self.connection = None

    def execute_query(self, query, params=None):
        """Execute a SQL query and return the results.
        :param query: SQL query to execute
        :param params: Optional parameters for the query
        :return: Query results as a list of tuples
        """
        if not self.connection:
            raise RuntimeError("Database connection is not established.")
        cursor = self.connection.cursor()
        cursor.execute(query, params or [])
        return cursor.fetchall()

    def query_table(self, table_name, columns='*', where=None):
        """Query a table in the database.
        :param table_name: Name of the table to query
        :param columns: Columns to select (default is all columns)
        :param where: Optional WHERE clause for filtering results
        :return: Query results as a list of tuples
        """
        query = f"SELECT {columns} FROM {table_name}"
        if where:
            query += f" WHERE {where}"
        return self.execute_query(query)

    def insert_into_table(self, table_name, columns, values):
        """Insert values into a table.
        :param table_name: Name of the table to insert into
        :param columns: Columns to insert values into
        :param values: Values to insert as a tuple or list
        """
        placeholders = ', '.join(['?'] * len(values))
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        self.execute_query(query, values)

    def commit(self):
        """Commit the current transaction to the database.
        This is necessary to save changes made by insert, update, or delete
        operations.
        """
        if self.connection:
            self.connection.commit()
