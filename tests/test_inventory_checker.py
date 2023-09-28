import pytest

from src.api_client import ApiClient
from src.inventory_checker import inventoryService


@pytest.fixture
def service(api_client):
    api_client = ApiClient()
    return inventoryService(api_client)


def test_user_can_build_set(service):
    user_inventory = {"3023": {"red": 4, "blue": 6}, "4286": {"red": 2, "white": 1}}
    set_pieces = [
        {"part": {"designID": "3023", "material": "blue"}, "quantity": 4},
        {"part": {"designID": "4286", "material": "red"}, "quantity": 2},
    ]
    assert service.user_can_build_set(user_inventory, set_pieces)


def test_user_can_build_set_missing_piece(service):
    user_inventory = {"3023": {"red": 4, "blue": 6}}  # Missing '4286'
    set_pieces = [
        {"part": {"designID": "3023", "material": "blue"}, "quantity": 4},
        {"part": {"designID": "4286", "material": "red"}, "quantity": 2},
    ]
    assert not service.user_can_build_set(user_inventory, set_pieces)


def test_user_can_build_set_insufficient_quantity(service):
    user_inventory = {"3023": {"red": 4, "blue": 3}}  # Insufficient quantity of 'blue'
    set_pieces = [
        {"part": {"designID": "3023", "material": "blue"}, "quantity": 4},
    ]
    assert not service.user_can_build_set(user_inventory, set_pieces)
