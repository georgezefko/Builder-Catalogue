# contain the logic to interact with the provided API endpoints.
import os

import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.environ.get("API")


def get_users():
    response = requests.get(f"{BASE_URL}/users")
    return response.json()


def get_user_by_username(username):
    """
    This function fetches a user's summary information based on their username.
    The returned information includes user id, username, location, and brickCount
    (number of different bricks the user owns).
    Response example: {'id': '123', 'username': 'brickfan35', 'location': 'UKY', 'brickCount': 1413}
    """
    response = requests.get(f"{BASE_URL}/user/by-username/{username}")
    return response.json()


def get_user_by_id(id):

    """
    This function fetches the detailed information of a user based on their user id.
    The returned information includes user id, username, location, brickCount
    and the user's collection which holds the piece id, color and count of each piece they own.
    Response example: {'id': '123', 'username': 'brickfan35', 'location': 'UKY', 'brickCount': 1413, 'collection': [...]}
    """
    response = requests.get(f"{BASE_URL}/user/by-id/{id}")
    return response.json()


def get_sets():
    """
    This function fetches a list of all available sets in the catalogue.
    The returned information for each set includes its id, name, setNumber, and totalPieces.
    Response example: {'Sets': [{'id': '1', 'name': 'alien-spaceship', 'setNumber': '497XX', 'totalPieces': 1050}, ...]}
    """
    response = requests.get(f"{BASE_URL}/sets")
    return response.json()


def get_set_by_name(set_name):
    """
    This function fetches a set's summary information based on its name.
    The returned information includes its id, name, setNumber, and totalPieces
    Response example: {'id': '1', 'name': 'treasure-caves', 'setNumber': '343XX', 'totalPieces': 1460}
    """
    response = requests.get(f"{BASE_URL}/set/by-name/{set_name}")
    return response.json()


def get_set_by_id(set_id):
    """
    This function fetches the detailed information of a set based on its id.
    The returned information includes the id, name, setNumber, totalPieces,
    and a list of pieces required to build the set, each with its designID, material, partType, and quantity.
    Response example: {'id': '1', 'name': 'treasure-caves', 'setNumber': '343XX', 'pieces': [...], 'totalPieces': 1460}
    """
    response = requests.get(f"{BASE_URL}/set/by-id/{set_id}")
    return response.json()


def get_colors():
    """
    This function fetches the full list of available colors.
    The returned information for each color includes its name and code.
    Response example: {'colours': [{'name': 'White', 'code': 1}, ...]}
    """
    response = requests.get(f"{BASE_URL}/colours")
    return response.json()
