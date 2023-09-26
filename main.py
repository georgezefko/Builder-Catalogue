from src.inventory_checker import check_user_inventory

if __name__ == "__main__":
    username = "brickfan35"
    buildable_sets = check_user_inventory(username)
    print(f"{username} can build sets: {buildable_sets}")
