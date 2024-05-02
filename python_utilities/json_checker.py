import json
from dataclasses import asdict, dataclass, fields
from typing import Any, List

from json_encoder import my_prettier
from pydantic import BaseModel, ValidationError, create_model


def dataclass_to_pydantic(dc):
    field_definitions = {f.name: (f.type, ...) for f in fields(dc)}
    return create_model(dc.__name__ + "Pydantic", **field_definitions)


def dump_json(data, filename):
    with open(filename, "w") as file:
        json.dump(asdict(data), file, indent=2, separators=(", ", ": "), cls=my_prettier)


def validate_json(filename, pydantic_class):
    with open(filename, "r") as file:
        data_dict = json.load(file)

    try:
        validated_data = pydantic_class.parse_obj(data_dict)
        print("Validation successful!")
        return validated_data
    except ValidationError as e:
        print("Validation error occurred!")
        print(e.json(indent=2))  # Print detailed validation errors
        return None
