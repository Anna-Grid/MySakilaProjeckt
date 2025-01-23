# db.py

import mysql.connector
from mysql.connector import MySQLConnection as Connector
from dotenv import load_dotenv
from typing import Optional, List, Dict
from my_exceptions import DatabaseConnectionError, QueryExecutionError
import os
import sql_queries as sql

load_dotenv()

class MySakilaConnection:
    connection: Optional[Connector]
    cursor: Optional[mysql.connector.cursor.MySQLCursorDict]

    def __init__(self) -> None:
        self.connection = None
        self.cursor = None

    def __enter__(self) -> "MySakilaConnection":
        try:
            self.connection = mysql.connector.connect(
                host=os.getenv('DB_HOST'),
                user=os.getenv('DB_USER'),
                password=os.getenv('DB_PASSWORD'),
                database=os.getenv('DB_NAME')
            )
            self.cursor = self.connection.cursor(dictionary=True)
            return self
        except mysql.connector.Error as e:
            raise DatabaseConnectionError(f"Database connection error: {e}")

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()

    def execute_query(self, query: str, params: Optional[tuple] = None) -> List[Dict]:
        """
        Executes an SQL query and returns the results.
        """
        try:
            self.cursor.execute(query, params or ())
            return self.cursor.fetchall()
        except mysql.connector.Error as e:
            raise QueryExecutionError(f"Query execution error: {e}, {params}")

    def record_user_query(self, query_name: str) -> None:
        """
        Records or updates a user's query in the 'queries' table.

        :param query_name: The name of the query.
        """
        query = sql.sql_table_record
        try:
            self.cursor.execute(query, (query_name,))
            self.connection.commit()
        except mysql.connector.Error as e:
            raise QueryExecutionError(f"Error executing query: {e}")

    def get_most_popular_queries(self) -> List[Dict]:
        """
        Returns the top 10 most popular queries.
        """
        query = sql.sql_popular_queries
        return self.execute_query(query)
