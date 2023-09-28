from src.api_client import ApiClient


class collaborationService:
    def __init__(self, api_client=ApiClient):
        self.api_client = api_client

    def get_user_inventory(self, username):
        user = self.api_client.get_user_by_username(username)
        user_id = self.api_client.get_user_by_id(user["id"])
        user_collection = user_id.get("collection", {})

        inventory = {}

        for piece in user_collection:

            piece_id = piece["pieceId"]

            for variant in piece["variants"]:
                color = variant["color"]
                count = variant["count"]

                if piece_id not in inventory:
                    inventory[piece_id] = {}

                inventory[piece_id][color] = count

        return inventory

    def get_sets_inventory(self, set_name):
        set_info = self.api_client.get_set_by_name(set_name)
        set_details = self.api_client.get_set_by_id(set_info["id"])
        set_pieces = set_details.get("pieces", [])
        inventory = {}
        for piece_info in set_pieces:
            piece = piece_info.get("part", {})
            design_id = piece.get("designID")
            material = piece.get("material")
            quantity = piece_info.get("quantity", 0)

            if not design_id or not material:
                continue  # Skip if designID or material is missing

            if design_id not in inventory:
                inventory[design_id] = {}

            inventory[design_id][material] = quantity

        return inventory

    def can_complete_set(self, inventories, set_inventory):
        combined = {}
        for inv in inventories:

            for piece_id, colors in inv.items():

                for color, count in colors.items():

                    if piece_id not in combined:
                        combined[piece_id] = {}

                    if color not in combined[piece_id]:
                        combined[piece_id][color] = 0

                    combined[piece_id][color] += count

        for piece_id, colors in set_inventory.items():

            for color, count in colors.items():

                if piece_id in combined and color in combined[piece_id]:
                    combined_count = combined[piece_id][color]
                else:
                    combined_count = 0
                # Check if the combined inventory has enough count of each piece and color
                if combined_count < count:
                    return False
        return True

    def get_collaboration(self, user_name, set_name):

        user_inventory = self.get_user_inventory(user_name)
        set_inventory = self.get_sets_inventory(set_name)

        users = [
            user["username"]
            for user in self.api_client.get_users()["Users"]
            if user["username"] != user_name
        ]
        helpers = []
        for helper_username in users:
            helper_inventory = self.get_user_inventory(helper_username)
            if self.can_complete_set([user_inventory, helper_inventory], set_inventory):
                helpers.append(helper_username)

        print(helpers)
        return helpers
