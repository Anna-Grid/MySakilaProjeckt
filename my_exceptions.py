# my_exceptions.py

class DatabaseConnectionError(Exception):
    """
    Exception raised for database connection issues.
    """
    def __init__(self, message, error_code=None):
        super().__init__(message)
        self.error_code = error_code  # Код ошибки, если доступен

    def __str__(self):
        if self.error_code:
            return f"{self.args[0]} (Error Code: {self.error_code})"
        return self.args[0]


class QueryExecutionError(Exception):
    """
    Exception raised for errors in executing SQL queries.
    """
    def __init__(self, message, query=None, error_code=None):
        super().__init__(message)
        self.query = query  # SQL-запрос, который вызвал ошибку (если доступен)
        self.error_code = error_code  # Код ошибки, если доступен

    def __str__(self):
        parts = [self.args[0]]
        if self.query:
            parts.append(f"(Query: {self.query})")
        if self.error_code:
            parts.append(f"(Error Code: {self.error_code})")
        return ' '.join(parts)

