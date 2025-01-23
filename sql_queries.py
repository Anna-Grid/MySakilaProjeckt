# Query new movies by rating
sql_query_rating = """
        SELECT title, release_year
        FROM film
        WHERE rating = %s
        ORDER BY release_year DESC
        LIMIT 10
    """

# Query by keyword in title or in description
sql_query_keyword = """
        SELECT title, release_year
        FROM film
        WHERE LOWER(title) LIKE %s OR LOWER(description) LIKE %s
        LIMIT 10
    """

# Query by genre and release year
sql_query_genre_year = """
        SELECT f.title, f.release_year
        FROM film AS f
        JOIN film_category AS fc ON f.film_id = fc.film_id
        JOIN category AS ca ON fc.category_id = ca.category_id
        WHERE LOWER(ca.name) = %s
        AND f.release_year = %s
        LIMIT 10
    """

# Query by actor's name and release year
sql_query_actor_year = """
        SELECT f.title, f.release_year, CONCAT(a.first_name, ' ', a.last_name) AS actor_name
        FROM film AS f
        JOIN film_actor AS fa ON f.film_id = fa.film_id
        JOIN actor AS a ON fa.actor_id = a.actor_id
        WHERE (LOWER(CONCAT(a.last_name, a.first_name)) LIKE %s
        OR LOWER(CONCAT(a.first_name, a.last_name)) LIKE %s)
        AND f.release_year = %s
        LIMIT 10
    """

# Query to insert a user request into a table
sql_table_record = """
            INSERT INTO queries (query_name, execution_count)
            VALUES (%s, 1)
            ON DUPLICATE KEY UPDATE execution_count = execution_count + 1
        """

# Output of the top-10 popular requests
sql_popular_queries = """
        SELECT query_name, execution_count
        FROM queries
        ORDER BY execution_count DESC
        LIMIT 10
        """