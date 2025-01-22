# db.py

import mysql.connector
from mysql.connector import MySQLConnection as Connector
from dotenv import load_dotenv
from typing import Optional, List, Dict
from my_exceptions import DatabaseConnectionError, QueryExecutionError
import os

load_dotenv()

class MySakilaConnection:
    connection: Optional[Connector]
    cursor: Optional[mysql.connector.cursor.MySQLCursorDict]
    
    def __init__(self) -> None:
        self.connection = None
        self.cursor = None

    def __enter__(self) -> "MySQLConnection":
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

    def execute_query(self, query: str, params: Optional[tuple]=None) -> List[Dict]:
        """
        Executes an SQL query and returns the results.
        """
        try:
            self.cursor.execute(query, params or ())
            return self.cursor.fetchall()
        except mysql.connector.Error as e:
            raise QueryExecutionError(f"Query execution error: {e}, {params}")


    def record_user_query(self, genre: str, actor: str, key_word: str, release_year: int, rating: int, execution_count: int) -> None:
        """
        Records or updates the user's query in the 'queries' table.

        :param genre: The genre of the movie.
        :param actor: The actor's name.
        :param key_word: The keyword.
        :param release_year: The release year of the movie.
        :param rating: The rating of the movie.
        :param execution_count: The number of times the query has been executed.
        """
        query = """
            INSERT INTO queries (genre, actor, key_word, release_year, rating, execution_count)
            VALUES (%s, %s, %s, %s, %s, 1)
            ON DUPLICATE KEY UPDATE execution_count = execution_count + 1;
        """
        params = (genre, actor, key_word, release_year, rating)

        with self.connection.cursor() as cursor:
            cursor.execute(query, params)

        self.connection.commit()


    def get_most_popular_queries(self):
        """
        Returns the rating of the most popular queries.
        """
        query = """
        SELECT COUNT(*), genre, actor, key_word, release_year, rating, execution_count
        FROM queries
        GROUP BY genre, actor, key_word, rating
        ORDER BY execution_count DESC
        LIMIT 10
        """
        return self.execute_query(query)
        