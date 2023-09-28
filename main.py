import argparse

from src.api_client import ApiClient
from src.collaboration_checker import collaborationService
from src.inventory_checker import inventoryService


def main():
    parser = argparse.ArgumentParser(description="Building Sets Checker")
    parser.add_argument("--username", default="brickfan35", help="Username to check")
    parser.add_argument(
        "--setname", default="tropical-island", help="Set name for collaboration check"
    )
    parser.add_argument("--service", default="check_inventory", help="Set service name")

    args = parser.parse_args()
    api_client = ApiClient()
    inventory_service = inventoryService(api_client)
    collaboration_service = collaborationService(api_client)

    if args.service == "check_inventory":
        sets = inventory_service.check_user_inventory(args.username)
        print(f"{args.username} can build {', '.join(sets)}")

    else:
        helpers = collaboration_service.get_collaboration(args.username, args.setname)
        print(
            f"{args.username} can complete the set with help from {', '.join(helpers)}"
        )


if __name__ == "__main__":
    main()
