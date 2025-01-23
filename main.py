# main.py

import func
import ui
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


def main() -> None:
    """
    The main function of the program for user interaction.
    """
    
    ui.display_menu()
    choice: str = ui.get_user_choice()

    try:
        if choice == '1':
            rating = ui.get_rating()
            movies = func.search_movies_by_rating(rating)
            func.display_movies_table(movies)
            record_queries_from_movies(f"Rating: {rating}")

        elif choice == '2':
            keyword = ui.get_keyword()
            movies = func.search_movies_by_keyword(keyword)
            func.display_movies_table(movies)
            record_queries_from_movies(f"Keyword: {keyword}")

        elif choice == '3':
            genre, year = ui.get_genre_and_year()
            movies = func.search_movies_by_genre_and_year(genre, year)
            func.display_movies_table(movies)
            record_queries_from_movies(f"Genre: {genre}; Year: {year}")

        elif choice == '4':
            actor, year = ui.get_actor_and_year()
            movies = func.search_movies_by_actor_and_year(actor, year)
            func.display_movies_actors_table(movies)
            user_input = f"Actor: {actor.title()}; Year: {year}"
            record_queries_from_movies(f"Actor: {actor.title()}; Year: {year}")

        elif choice == '5':
            popular_queries = func.get_popular_queries()
            if popular_queries:
                print("Popular queries:")
                func.display_table(popular_queries)
            else:
                print("No popular queries found.")
        else:
            raise ValueError("Invalid scenario selection.")
    except Exception as e:
        print(f"Error: {e}")


def record_queries_from_movies(query_name: str) -> None:
    """
    Records a query in the database.

    :param query_name: The name of the query to record.
    """
    func.record_user_query(query_name)


if __name__ == "__main__":
    main()