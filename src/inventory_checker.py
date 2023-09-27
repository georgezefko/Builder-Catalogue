import json
import os

from src.api_client import get_colors
from src.api_client import get_set_by_id
from src.api_client import get_sets
from src.api_client import get_user_by_id
from src.api_client import get_user_by_username


def format_pieces_for_set(set_pieces, colors):
    formatted_pieces = []
    for piece in set_pieces:
        color_code = str(piece["part"]["material"])
        color_name = next(
            (color["name"] for color in colors if str(color["code"]) == color_code),
            "Unknown Color",
        )
        part_number = str(piece["part"]["designID"])
        quantity = piece["quantity"]
        formatted_pieces.append(
            {"Quantity": quantity, "Part Number": part_number, "Color": color_name}
        )

    return formatted_pieces


def user_can_build_set(user_inventory, set_pieces):
    for piece in set_pieces:
        design_id = str(piece["part"]["designID"])
        material = str(piece["part"]["material"])
        quantity = piece["quantity"]
        if (
            design_id not in user_inventory
            or material not in user_inventory[design_id]
            or user_inventory[design_id][material] < quantity
        ):
            return False
    return True


def save_pieces_to_file(set_name, formatted_pieces):
    folder_name = "results"
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    filename = f"{folder_name}/{set_name.replace(' ', '_')}_pieces.json"
    with open(filename, "w") as f:
        json.dump(formatted_pieces, f)


def check_user_inventory(user_name):
    user = get_user_by_username(user_name)
    user_id = get_user_by_id(user["id"])
    user_collection = user_id.get("collection", {})

    user_inventory = {}
    for piece in user_collection:

        piece_id = piece["pieceId"]

        for variant in piece["variants"]:
            color = variant["color"]
            count = variant["count"]

            if piece_id not in user_inventory:
                user_inventory[piece_id] = {}

            user_inventory[piece_id][color] = count

    available_sets = get_sets()
    colors = get_colors()["colours"]

    for set in available_sets["Sets"]:
        set_id = set["id"]
        set_name = set["name"]
        set_data = get_set_by_id(set_id)
        set_pieces = set_data["pieces"]

        if user_can_build_set(user_inventory, set_pieces):
            formatted_pieces = format_pieces_for_set(set_pieces, colors)
            save_pieces_to_file(set_name, formatted_pieces)

    return
