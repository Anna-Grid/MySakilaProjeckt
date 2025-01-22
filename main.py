# main.py

import func
import ui
from user_exceptions import UserInputError, MovieNotFoundError
from my_exceptions import DatabaseConnectionError, QueryExecutionError
from db import MySakilaConnection
from typing import List, Dict, Union, Tuple


def display_movies(movies: List[Dict]) -> None:
    """
    Displays a list of found movies.
    """
    if movies:
        print("")
        for movie in movies:
            print(f"Title: {movie['title']}, Year: {movie.get('release_year')}")
    else:
        print("No movies found.")


def handle_error(e: Exception) -> None:
    """
    Displays an error with the corresponding message.
    """
    print(f"Error: {e}")


def record_user_query(genre: str, actor: str, key_word: str, release_year: int, rating: int, execution_count: int) -> None:
    """
    Records the user's query in the queries table.
    """
    try:
        with MySakilaConnection() as base:
            base.record_user_query(
                genre, actor, key_word, release_year, rating, execution_count
            )
    except (DatabaseConnectionError, QueryExecutionError) as e:
        print(f"Error while recording the query in the database. {e}") # перенести в setting


def main() -> None:
    """
    The main function of the program for user interaction.
    """
    
    ui.display_menu()
    choice: str = ui.get_user_choice()

    try:
        if choice == '1':
            rating: int = ui.get_rating()
            movies: List[Dict[str, Union[str, int]]] = func.search_movies_by_rating(rating)
            func.display_movies_table(movies)

            record_queries_from_movies(movies, rating=rating)


        elif choice == '2':
            keyword: str = ui.get_keyword()
            movies: List[Dict[str, Union[str, int]]] = func.search_movies_by_keyword(keyword)
            func.display_movies_table(movies)

            record_queries_from_movies(movies, keyword=keyword)    

        
        elif choice == '3':
            genre: str = ''
            year: int = 0
            genre, year = ui.get_genre_and_year()
            movies: List[Dict[str, Union[str,int]]] = func.search_movies_by_genre_and_year(genre, year)
            func.display_movies_table(movies)

            record_queries_from_movies(movies, genre=genre, release_year=year)

        
        elif choice == '4':
            actor: str = ''
            year: int = 0
            actor, year = ui.get_actor_and_year()
            movies: List[Dict[str, Union[str, int]]] = func.search_movies_by_actor_and_year(actor, year)
            func.display_movies_table(movies)

            record_queries_from_movies(movies, actor=actor, release_year=year)

        
        elif choice == '5':
            popular_queries: List[Dict[str, Union[str, int]]] = func.get_popular_queries()
            print("Popular queries:")
            func.display_table(popular_queries)


        else:
            raise UserInputError("Invalid scenario selection.")

    except (UserInputError, MovieNotFoundError) as e:
        handle_error(e)
    except (DatabaseConnectionError, QueryExecutionError) as e:
        handle_error(e)


def record_queries_from_movies(movies: List[Dict[str, Union[str, int]]], **kwargs) -> None:
    """
    Records a list of movie queries in the database, taking into account the provided parameters.

    :param movies: List of found movies.
    :param kwargs: Additional query parameters (genre, actor, key_word, release_year, rating).
    """
    for movie in movies:
        query_params = {
            'genre': movie.get('genre', kwargs.get('genre', '')),
            'actor': movie.get('actor', kwargs.get('actor', '')),
            'key_word': movie.get('keyword', kwargs.get('key_word', '')),
            'release_year': movie.get('year', kwargs.get('release_year')),
            'rating': movie.get('rating', kwargs.get('rating')),
        }
        # Передаем параметры как отдельные аргументы
        with MySakilaConnection() as base:
            base.record_user_query(
                query_params['genre'], 
                query_params['actor'], 
                query_params['key_word'], 
                query_params['release_year'], 
                query_params['rating'], 
                1  # значение execution_count, которое будет всегда равно 1
            )


def parse_query(query: str) -> Tuple[str, str, str, int, int]:
    """
    Parses the query string into individual elements.

    :param query: Query string in the format 'genre actor keyword release_year rating'.
    :return: A tuple containing the genre, actor, keyword, year, and rating.
    """
    parts = query.split(' ')
    genre = parts[0] if len(parts) > 0 else ''
    actor = parts[1] if len(parts) > 1 else ''
    keyword = parts[2] if len(parts) > 2 else ''
    release_year = int(parts[3]) if len(parts) > 3 and parts[3].isdigit() else None
    rating = int(parts[4]) if len(parts) > 4 and parts[4].isdigit() else None
    return genre, actor, keyword, release_year, rating



if __name__ == "__main__":
    main()