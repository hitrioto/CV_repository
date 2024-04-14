from dataclasses import dataclass, fields, asdict
from pydantic import BaseModel, create_model, ValidationError
from typing import List, Any
import json
from json_checker import dataclass_to_pydantic, dump_json, validate_json

@dataclass
class TestClass:
    a_2D_list: List[List[int]]
    a_1D_list: List[int]


if __name__ == "__main__":
    # Define the Pydantic model class based on the dataclass
    TestClassPydantic = dataclass_to_pydantic(TestClass)

    # Example usage
    example_class = TestClass(a_2D_list=[[1, 2], [3, 4]], a_1D_list=[1, 2, [3]])
    my_file = "test_json_checker.json"

    dump_json(example_class, my_file)
    validated_data = validate_json(my_file, TestClassPydantic)
    print(validated_data)