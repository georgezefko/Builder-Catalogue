# Builder-Catalogue

## Overview

Which sets can the user brickfan35 build with their exisiting inventory of pieces?

## Solution Logic

The solution involves the following logical steps:

- Retrieve user’s collection data.
- Retrieve the set’s pieces data.
- Compare the user's collection with the set's required pieces.
- Determine if the user has sufficient pieces to build the set.

## API Functions

Each API function interacts with a corresponding API endpoint to fetch necessary information:

- get_user_by_username(username): Fetches a user's summary information based on their username. Returns user id, username, location, and brickCount.
- get_user_by_id(user_id): Fetches detailed information of a user based on their user id. Returns user id, username, location, brickCount, and the user’s collection with piece id, color, and count of each piece they own.
- get_sets(): Fetches a list of all available sets in the catalogue. Returns each set’s id, name, setNumber, and totalPieces.
- get_set_by_id(set_id): Fetches detailed information of a set based on its id. Returns id, name, setNumber, totalPieces, and a list of pieces required to build the set, each with its designID, material, partType, and quantity.
- get_set_by_name(name): Fetches a set's summary information based on its name. Returns its id, name, setNumber, and totalPieces.
- get_colors(): Fetches the full list of available colors. Returns each color’s name and code.
Implementation

High-level view of the logic implementation:

- User Collection Retrieval: Using get_user_by_id, the user's collection is retrieved, which includes the details of each piece and its count that the user owns.
- Set Pieces Retrieval: Using get_set_by_id, the pieces required for the desired set are retrieved, which includes the details of each piece and its required quantity.
- Collection and Set Comparison: The user's collection is then compared to the set’s required pieces. For each piece required by the set, the system checks whether the user’s collection contains that piece and whether the quantity owned is sufficient.
- Result Determination: If the user's collection contains all the required pieces in sufficient quantities, the system confirms that the user can build the set. Otherwise, the system identifies the missing pieces or those in insufficient quantity.
