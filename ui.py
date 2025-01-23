# ui.py

from typing import Tuple
from db import MySakilaConnection
import setting as se
import sys


def display_menu():
    """
    Displays the search scenario selection menu.
    """
    print('Select a search scenario:')
    print('\n'.join(se.MENU_ITEMS))
    

def get_user_choice() -> int:
    """
    Gets the user's selection.
    """
    while True:
        choice = input(f"Enter the scenario number. (1-{len(se.SCENARIO_SET)}): ").strip()
        if choice in se.SCENARIO_SET:
            return choice
        print(f"Error: Please select a number from 1 to {len(se.SCENARIO_SET)}.")


def get_rating() -> int:
    """
    Gets the rating from the user.
    """
       
    while True:
        try:
            rating = int(input(f'''Enter the rating.:
                    {se.RATING_TEXT}
                    '''))
            if not 1 <= rating <= se.RATING_LEN:
                print(f"Error: Please enter a numerical rating (1 - {se.RATING_LEN}).")
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
        actor = input("Enter the actor's name: ").replace(" ", "")
        if not actor:
            print("Error: The name cannot be empty!")
            continue
        try:
            year = int(input("Enter the year: "))
            if year <= 0:
                print("Error: The year must be a positive number.")
            else:
                return actor, year
        except ValueError:
            print("Error: Please enter the year in numeric format.")


def get_exit():
    """
    Displays a goodbye message and exits the application.
    """
    print("\nThank you for using the Movie Database. Goodbye!")
    sys.exit(0) 
        