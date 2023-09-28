import json
import os

from src.api_client import ApiClient


class inventoryService:
    def __init__(self, api_client: ApiClient):
        self.api_client = api_client

    def user_can_build_set(self, user_inventory, set_pieces):
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

    def save_pieces_to_file(self, set_name, user_name):
        folder_name = "results"
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
        filename = f"{folder_name}/{user_name.replace(' ', '_')}_sets.json"
        with open(filename, "w") as f:
            json.dump(set_name, f)

    def check_user_inventory(self, user_name):
        user = self.api_client.get_user_by_username(user_name)
        user_id = self.api_client.get_user_by_id(user["id"])
        user_collection = user_id.get("collection", {})

        user_inventory = {}
        set_names = []
        for piece in user_collection:

            piece_id = piece["pieceId"]

            for variant in piece["variants"]:
                color = variant["color"]
                count = variant["count"]

                if piece_id not in user_inventory:
                    user_inventory[piece_id] = {}

                user_inventory[piece_id][color] = count

        available_sets = self.api_client.get_sets()

        for set in available_sets["Sets"]:
            set_id = set["id"]
            set_name = set["name"]
            set_data = self.api_client.get_set_by_id(set_id)
            set_pieces = set_data["pieces"]

            if self.user_can_build_set(user_inventory, set_pieces):
                set_names.append(set_name)

        self.save_pieces_to_file(set_names, user_name)

        return set_names
