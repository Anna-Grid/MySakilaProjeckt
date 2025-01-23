# func.py

from db import MySakilaConnection
from typing import List, Dict, Union
import sql_queries as sql
from user_exceptions import MovieNotFoundError


def search_movies_by_rating(rating: int) -> List[Dict[str, Union[str, int]]]:
    """
    Searches for movies by rating.
    """
    sql_query = sql.sql_query_rating
    with MySakilaConnection() as base:
        results = base.execute_query(sql_query, (rating,))
    if not results:
        raise MovieNotFoundError(f"Movies rating '{rating}' not found.")
    return results


def search_movies_by_keyword(keyword: str) -> List[Dict[str, Union[str, int]]]:
    """
    Searches for movies by keyword.
    """
    sql_query = sql.sql_query_keyword
    with MySakilaConnection() as base:
        results = base.execute_query(sql_query, (f"%{keyword.lower()}%", f"%{keyword.lower()}%"))
    if not results:
        raise MovieNotFoundError(f"Movies with the keyword '{keyword}' not found.")
    return results


def search_movies_by_genre_and_year(genre: str, year: int) -> List[Dict]:
    """
    Searches for movies by genre and year.
    """
    sql_query = sql.sql_query_genre_year
    with MySakilaConnection() as base:
        results = base.execute_query(sql_query, (genre.lower(), year))
    if not results:
        raise MovieNotFoundError(f"Movies with the genre '{genre}' and release year {year} not found.")
    return results


def search_movies_by_actor_and_year(actor: str, year: int) -> List[Dict]:
    """
    Searches for movies by actor and year.
    """
    sql_query = sql.sql_query_actor_year
    actor_name = f"%{actor.lower()}%" if actor else ""
    with MySakilaConnection() as base:
        results = base.execute_query(sql_query, (actor_name, actor_name, year))
    if not results:
        raise MovieNotFoundError(f"Movies with actor '{actor.title()}' and release year {year} not found.")
    return results


def record_user_query(query_name: str) -> None:
    """
    Records or updates the user's query in the database.
    """
    with MySakilaConnection() as base:
        base.record_user_query(query_name)


def get_popular_queries() -> List[Dict[str, Union[str, int]]]:
    """
    Returns the top 10 most popular queries with their execution counts.
    """
    with MySakilaConnection() as base:
        result = base.get_most_popular_queries()

    queries_with_description = []
    for row in result:
        queries_with_description.append({
            "query": row['query_name'],
            "count": row['execution_count']
        })

    return queries_with_description

    #----------------------------------------------------------------------

def display_table(data: List[Dict[str, Union[str, int]]]) -> None:
    """
    Displays data in a table format using symbols.

    :param data: A list of dictionaries with keys 'query' and 'count'.
    """
    if not data:
        print("No data to display.")
        return

    query_header = "Queries"
    count_header = "Counts"
    
    query_width = max(len(row['query']) for row in data) + 1 if data else len(query_header) + 1
    count_width = len(count_header) + 0
    
    print('-' * (query_width + count_width + 7))
    print(f"| {query_header.ljust(query_width)} | {count_header.rjust(count_width)} |")
    print('-' * (query_width + count_width + 7))
    
    for row in data:
        query = row['query'].ljust(query_width)
        count = str(row['count']).rjust(count_width)
        print(f"| {query} | {count} |")
    
    print('-' * (query_width + count_width + 7))


def display_movies_table(movies: List[Dict[str, Union[str, int]]]) -> None:
    """
    Displays a list of movies in a table format using symbols.

    :param movies: A list of dictionaries with keys 'title' and 'release_year'.
    """
    title_header = "Movies"
    year_header = "Release Year"
    
    title_width = max(len(movie['title']) for movie in movies) + 2 if movies else len(title_header) + 2
    year_width = len(year_header) + 2
    
    print('-' * (title_width + year_width + 7))
    print(f"| {title_header.ljust(title_width)} | {year_header.rjust(year_width)} |")
    print('-' * (title_width + year_width + 7))
    
    for movie in movies:
        title = movie['title'].ljust(title_width)
        year = str(movie['release_year']).rjust(year_width)
        print(f"| {title} | {year} |")
    
    print('-' * (title_width + year_width + 7))


def display_movies_actors_table(movies: List[Dict[str, Union[str, int]]]) -> None:
    """
    Displays a list of movies and actors in a table format using symbols.

    :param movies: A list of dictionaries with keys 'title', 'release_year' and 'actor'.
    """
    title_header = "Movies"
    year_header = "Release Year"
    actor_header = "Actors"
    
    title_width = max(len(movie['title']) for movie in movies) + 2 if movies else len(title_header) + 2
    year_width = len(year_header) + 0
    actor_width = max(len(movie['actor_name']) for movie in movies) + 2 if movies else len(actor_header) + 2
    
    print('-' * (title_width + year_width + actor_width + 10))
    print(f"| {title_header.ljust(title_width)} | {year_header.rjust(year_width)} | {actor_header.ljust(actor_width)} |")
    print('-' * (title_width + year_width + actor_width + 10))
    
    for movie in movies:
        title = movie['title'].ljust(title_width)
        year = str(movie['release_year']).rjust(year_width)
        actor = movie['actor_name'].ljust(actor_width)
        print(f"| {title} | {year} | {actor} |")
    
    print('-' * (title_width + year_width + actor_width + 10))

