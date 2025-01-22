# func.py

from db import MySakilaConnection
from typing import List, Dict, Union
from user_exceptions import MovieNotFoundError


def search_movies_by_rating(rating: int) -> List[Dict[str, Union[str, int]]]: # ищет фильмы по рейтингу
    """
    Searches for movies by rating.
    """
    sql_query = """
        SELECT title, release_year
        FROM film
        WHERE rating = %s
        ORDER BY release_year DESC
        LIMIT 10
    """
    with MySakilaConnection() as base:
        results = base.execute_query(sql_query, (rating,))
    if not results:
        raise MovieNotFoundError(f"Movies rating '{rating}' not found.", movie_title=str(rating))
    return results

    
def search_movies_by_keyword(keyword: str) -> List[Dict]:
    """
    Searches for movies by keyword.
    """
    sql_query = """
        SELECT title, release_year
        FROM film 
        WHERE LOWER(title) LIKE %s OR LOWER(description) LIKE %s
        LIMIT 10
    """
    with MySakilaConnection() as base:
        results = base.execute_query(sql_query, (f'%{keyword.lower()}%', f'%{keyword.lower()}%'))
    if not results:
        raise MovieNotFoundError(f"Movies with the keyword '{keyword}' not found.")
    return results


def search_movies_by_genre_and_year(genre: str, year: int) -> List[Dict]:
    """
    Searches for movies by genre and year.
    """
    sql_query = """
        SELECT f.title, f.release_year
        FROM film AS f
        JOIN film_category AS fc ON f.film_id = fc.film_id
        JOIN category AS ca ON fc.category_id = ca.category_id
        WHERE LOWER(ca.name) = %s
        AND f.release_year = %s
        LIMIT 10
    """
    with MySakilaConnection() as base:
        results = base.execute_query(sql_query, (genre.lower(), year))
    if not results:
        raise MovieNotFoundError(f"Movies with the genre '{genre}' and release year {year} not found.")
    return results


def search_movies_by_actor_and_year(actor: str, year: int) -> List[Dict]:
    """
    Searches for movies by actor and year.
    """
    sql_query = """
        SELECT f.title, f.release_year
        FROM film AS f
        JOIN film_actor AS fa ON f.film_id = fa.film_id
        JOIN actor AS a ON fa.actor_id = a.actor_id
        WHERE LOWER(a.last_name) = %s
        AND f.release_year = %s
        LIMIT 10
    """
    with MySakilaConnection() as base:
        results = base.execute_query(sql_query, (actor.lower(), year))
    if not results:
        raise MovieNotFoundError(f"Movies with actor '{actor.title()}' and release year {year} not found.")
    return results


def get_popular_queries() -> List[Dict[str, Union[str, int]]]:
    """
    Returns the top 10 most popular queries with parameter descriptions.
    """
    sql_query = """
        SELECT 
            genre,
            actor,
            key_word,
            release_year,
            rating,
            SUM(execution_count) AS count
        FROM queries
        GROUP BY genre, actor, key_word, rating
        ORDER BY count DESC
        LIMIT 10
    """
    with MySakilaConnection() as base:
        result = base.execute_query(sql_query)
        
        queries_with_description = []
        for row in result:
            description = []
            if row['genre']:
                description.append(f"Genre: {row['genre']}")
            if row['actor']:
                description.append(f"Actor: {row['actor']}")
            if row['key_word']:
                description.append(f"Keyword: {row['key_word']}")
            if row['release_year']:
                description.append(f"Release year: {row['release_year']}")
            if row['rating']:
                description.append(f"Rating: {row['rating']}")
            
            queries_with_description.append({
                "query": "; ".join(description),
                "count": row['count']            
            })
        
        return queries_with_description


def get_movies_by_query(
    genre: str = "",
    actor: str = "",
    keyword: str = "",
    release_year: int = 0,
    rating: int = ""
) -> List[Dict[str, Union[str, int]]]:
    """
    Returns a list of movies that match the given query.

    :param genre: Movies genre.
    :param actor: Actor name.
    :param keyword: Keyword.
    :param release_year: Release year.
    :param rating: Rating.
    :return: List of movies in the form of dictionaries.
    """
    sql_query = """
        SELECT f.title, 
               c.name AS genre, 
               q.release_year,
               f.rating
        FROM film AS f
        JOIN film_category AS fc ON f.film_id = fc.film_id
        JOIN category AS c ON fc.category_id = c.category_id
        JOIN queries AS q ON 1 = 1
        WHERE (c.name LIKE %s OR %s = '')       -- Filter by genre
          AND (f.title LIKE %s OR %s = '')      -- Filter by title
          AND (q.key_word LIKE %s OR %s = '')   -- Filter by keyword
          AND (q.release_year = %s OR %s = '')  -- Filter by release year
          AND (f.rating = %s OR %s = '')        -- Filter by rating
    """
    
    genre_filter = None if not genre else genre
    actor_filter = None if not actor else actor
    keyword_filter = None if not keyword else keyword
    release_year_filter = 0 if not release_year else release_year
    rating_filter = None if not rating else rating


    with MySakilaConnection() as base:
        result = base.execute_query(
            sql_query,
            (
                f"%{genre_filter}%", genre_filter,
                f"%{actor_filter}%", actor_filter,
                f"%{keyword_filter}%", keyword_filter,
                release_year_filter, release_year_filter,
                rating_filter, rating_filter
            )
        )
       
        return [{"title": row[0], "genre": row[1], "release_year": row[2], "rating": row[3]} for row in result]



def display_table(data: List[Dict[str, Union[str, int]]]) -> None:
    """
    Выводит данные в виде таблицы с использованием символов.
    
    :param data: Список словарей с ключами 'query' и 'count'.
    """
    query_header = "Queries"
    count_header = "Counts"
    
    query_width = max(
        max(len(row['query']) for row in data) if data else 0, len("Queries")
    ) + 1
    
    count_width = max(
        max(len(str(row['count'])) for row in data) if data else 0, len("Counts")
    ) + 1
    
    print('-' * (query_width + count_width + 7))
    print(f"| {'Queries'.ljust(query_width)} | {'Counts'.rjust(count_width)} |")
    print('-' * (query_width + count_width + 7))
    
    for row in data:
        query = row['query'].ljust(query_width)
        count = str(row['count']).rjust(count_width)
        print(f"| {query} | {count} |")
    
    print('-' * (query_width + count_width + 7))


def display_movies_table(movies: List[Dict[str, Union[str, int]]]) -> None:
    """
    Отображает список фильмов в виде таблицы с использованием символов.
    
    :param movies: Список словарей с ключами 'title' и 'release_year'.
    """
    title_header = "Movies"
    year_header = "Release"
    
    title_width = max(
        max(len(row['title']) for row in movies) if movies else 0, len(title_header)
    ) + 2
    
    year_width = max(
        max(len(str(row['release_year'])) for row in movies) if movies else 0, len(year_header)
    ) + 2
    
    print('-' * (title_width + year_width + 7))
    print(f"| {'Movies'.ljust(title_width)} | {'Releas'.rjust(year_width)} |")
    print('-' * (title_width + year_width + 7))
    
    for movie in movies:
        title = movie['title'].ljust(title_width)
        year = str(movie['release_year']).rjust(year_width)
        print(f"| {title} | {year} |")
    
    print('-' * (title_width + year_width + 7))


