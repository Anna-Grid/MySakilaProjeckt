# user_exceptions.py

class UserInputError(Exception):
    """
    Exception raised for errors in user input.
    """
    def __init__(self, message, input_value=None):
        super().__init__(message)
        self.input_value = input_value  # Значение ввода, которое вызвало ошибку

    def __str__(self):
        if self.input_value is not None:
            return f"{self.args[0]} (Input Value: {self.input_value})"
        return self.args[0]


class MovieNotFoundError(Exception):
    """
    Exception raised when a movie is not found.
    """
    def __init__(self, message, movie_title=None):
        super().__init__(message)
        self.movie_title = movie_title  # Название фильма, которое не было найдено

    def __str__(self):
        if self.movie_title:
            return f"{self.args[0]} (Movie Title: {self.movie_title})"
        return self.args[0]
