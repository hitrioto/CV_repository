import json
from pathlib import Path

Data = list | dict | int | float | str


def get_object_by_keys(json_filename: str, keys: list[str]) -> Data | None:
    # Load the JSON data from the file
    with Path(json_filename).open(mode="r") as file:
        data = json.load(file)

    # Navigate through the nested dictionaries
    current_data = data
    for key in keys:
        # Check if the key exists at the current level
        if key in current_data:
            current_data = current_data[key]
        else:
            # Key doesn't exist, return an empty list
            return []

    return current_data
