from api_client import get_set_by_name
from api_client import get_user_by_username
from api_client import get_users


def get_user_inventory(username):
    user = get_user_by_username(username)
    inventory = {}
    for piece in user.get("collection", []):
        piece_id = piece["pieceId"]
        for variant in piece["variants"]:
            inventory.setdefault(piece_id, {}).setdefault(
                variant["color"], variant["count"]
            )
    return inventory


def get_sets_inventory(set_name):
    set_info = get_set_by_name(set_name)
    inventory = {}
    for piece in set_info.get("pieces", []):
        inventory.setdefault(piece["designID"], {}).setdefault(
            piece["material"], piece["quantity"]
        )
    return inventory


def get_missing_pieces(user_inventory, set_inventory):
    missing = {}
    for piece_id, colors in set_inventory.items():
        for color, count in colors.items():
            missing_count = count - user_inventory.get(piece_id, {}).get(color, 0)
            if missing_count > 0:
                missing.setdefault(piece_id, {}).setdefault(color, missing_count)
    return missing


def can_complete_set(inventories, set_inventory):
    combined = {}
    for inv in inventories:
        for piece_id, colors in inv.items():
            for color, count in colors.items():
                combined.setdefault(piece_id, {}).setdefault(color, 0)
                combined[piece_id][color] += count

    for piece_id, colors in set_inventory.items():
        for color, count in colors.items():
            if combined.get(piece_id, {}).get(color, 0) < count:
                return False
    return True


if __name__ == "__main__":
    user_name = "landscape-artist"
    set_name = "tropical-island"

    user_inventory = get_user_inventory(user_name)
    set_inventory = get_sets_inventory(set_name)
    missing_pieces = get_missing_pieces(user_inventory, set_inventory)

    users = [
        user["username"]
        for user in get_users()["Users"]
        if user["username"] != user_name
    ]
    potential_helpers = {user: get_user_inventory(user) for user in users}

    for user, inventory in potential_helpers.items():
        if can_complete_set([user_inventory, inventory], set_inventory):
            print(f"{user_name} can complete the set with help from {user}")
            # break
