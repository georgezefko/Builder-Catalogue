import pytest

from src.inventory_checker import check_user_inventory
from src.inventory_checker import format_pieces_for_set
from src.inventory_checker import user_can_build_set

# Consider using the @pytest.fixture decorator to create objects you can reuse in multiple test functions.
@pytest.fixture
def sample_user_inventory():
    return {"3023": {"red": 4, "blue": 6}, "4286": {"red": 2, "white": 1}}


@pytest.fixture
def sample_set_pieces():
    return [
        {"part": {"designID": "3023", "material": "blue"}, "quantity": 4},
        {"part": {"designID": "4286", "material": "red"}, "quantity": 2},
    ]


@pytest.fixture
def sample_colors():
    return [
        {"code": "red", "name": "Red"},
        {"code": "blue", "name": "Blue"},
        {"code": "white", "name": "White"},
    ]


def test_user_can_build_set(sample_user_inventory, sample_set_pieces):
    assert user_can_build_set(sample_user_inventory, sample_set_pieces) is True


def test_check_user_inventory(mocker, sample_user_inventory):
    mocker.patch("inventory_checker.get_user_by_username", return_value={"id": "1"})
    mocker.patch(
        "inventory_checker.get_user_by_id",
        return_value={"collection": sample_user_inventory},
    )
    mocker.patch("inventory_checker.get_sets", return_value={"Sets": []})
    assert check_user_inventory("test_user") == []


def test_format_pieces_for_set(sample_set_pieces, sample_colors):
    expected_result = ["4 x part number 3023 in Blue", "2 x part number 4286 in Red"]
    assert format_pieces_for_set(sample_set_pieces, sample_colors) == expected_result
