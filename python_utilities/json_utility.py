import json
from typing import Any, List, Optional

def get_object_by_keys(json_filename: str, keys: List[str]) -> Optional[List[Any]]:
    # Load the JSON data from the file
    with open(json_filename, "r") as file:
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
    # Ensure the output is always a list
    return [current_data] if isinstance(current_data, dict) else current_data