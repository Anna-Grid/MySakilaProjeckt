# ui.py

from typing import Tuple
from db import MySakilaConnection
import setting as se


def display_menu():
    """
    Displays the search scenario selection menu.
    """
    print('Select a search scenario:')
    print('\n'.join(se.menu_items))

def get_user_choice() -> str:
    """
    Gets the user's selection.
    """
    while True:
        choice = input("Enter the scenario number. (1-5): ")
        if choice in ['1', '2', '3', '4', '5']:
            return choice
        print("Error: Please select a number from 1 to 5.")

# доработать функцию и использовать для вывода в main.py
def get_rating() -> int:
    """
    Gets the rating from the user.
    """
       
    while True:
        try:
            rating = int(input('''Enter the rating.:
                    1. "General Audiences"
                    2. "Parental Guidance Suggested"
                    3. "Parents Strongly Cautioned"
                    4. "Restricted"
                    5. "No One 17 and Under Admitted"
                    '''))
            if not 1 <= rating <= 5:
                print("Error: Please enter a numerical rating (1 - 5).")
            else:
                return rating
        except ValueError:
            print("Error: Please enter the rating in numeric format.")


def get_keyword() -> str:
    """
    Gets the keyword from the user.
    """
    keyword = input("Enter the keyword: ").strip()
    if not keyword:
        print("Error: The keyword cannot be empty!")
    else:
        return keyword


def get_genre_and_year() -> Tuple[str, int]:
    """
    Gets the genre and year from the user.
    """
    while True:
        genre = input("Enter the genre: ").strip()
        if not genre:
            print("Error: The genre cannot be empty!")
            continue
        try:
            year = int(input("Enter the year: "))
            if year <= 0:
                print("Error: The year must be a positive number.")
            else:
                return genre, year
        except ValueError:
            print("Error: Please enter the year in numeric format.")


def get_actor_and_year() -> Tuple[str, int]:
    """
    Gets the actor's name and year from the user.
    """
    while True:
        actor = input("Enter the actor's name: ").strip()
        if not actor:
            print("Error: The name cannot be empty!")
            continue
        try:
            year = int(input("Enter the year:"))
            if year <= 0:
                print("Error: The year must be a positive number.")
            else:
                return actor, year
        except ValueError:
            print("Error: Please enter the year in numeric format.")
            

def record_user_query_in_database(genre: str, actor: str, key_word: str, release_year: int, rating: int) -> None:
    """
    Recording the user's query in the queries table.
    """
    with MySakilaConnection() as base:
        base.record_user_query(genre, actor, key_word, release_year, rating)
        print("The query has been successfully added to the database.")


# def search_movies():
#     """
#     Query for selecting a search scenario and adding the query to the database.
#     """
#     display_menu()
#     scenario = get_user_choice()

#     if scenario == '1':
#         # Search by rating
#         keyword = get_keyword()
#         record_user_query_in_database("", "", "", 0, rating)

#     if scenario == '2':
#         # Search by Keyword
#         keyword = get_keyword()
#         record_user_query_in_database("", "", keyword, 0, None)

#     elif scenario == '3':
#         # Search by genre and year
#         genre, year = get_genre_and_year()
#         record_user_query_in_database(genre, "", "", year, None)

#     elif scenario == '4':
#         # Search by actor and year
#         actor, year = get_actor_and_year()
#         record_user_query_in_database("", actor, "", year, None)

#     elif scenario == '5':
#         # Search by popular queries
#         print("Popular queries")
#         with MySakilaConnection() as base:
#             queries = base.get_most_popular_queries()
#             for query in queries:
#                 print(
#                     f"Title: {query['film_title']}, Actor: {query['actor']}, "
#                     f"Keyword: {query['key_word']}, Year: {query['release_year']}, "
#                     f"Rating: {query['rating']}, Count: {query['execution_count']}"
#                 )

#     else:
#         print("Invalid scenario selection!")

# if __name__ == "__main__":
#     search_movies()