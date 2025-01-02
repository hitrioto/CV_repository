import json
import os
from collections import defaultdict
from typing import Any, Dict, List

from jinja2 import Template

class_definitions = defaultdict(str)  # To hold all class definitions


def infer_type(value, field_name):
    if isinstance(value, dict):
        class_name = f"{field_name.capitalize()}Class"
        process_class(value, class_name)
        return class_name
    elif isinstance(value, list):
        element_type = infer_type(value[0], field_name) if value else "Any"
        return f"List[{element_type}]"
    elif isinstance(value, int):
        return "int"
    elif isinstance(value, float):
        return "float"
    elif isinstance(value, bool):
        return "bool"
    elif value is None:
        return "Any"
    else:
        return "str"


def process_class(data: Dict[str, Any], class_name: str):
    fields = {key: infer_type(value, key) for key, value in data.items()}
    template_str = """\
@dataclass
class {{ class_name }}:
{%- for field, type in fields.items() %}
    {{ field }}: {{ type }}
{%- endfor %}
"""
    template = Template(template_str)
    class_definitions[class_name] = template.render(
        class_name=class_name, fields=fields
    )


def generate_dataclass(json_data: str, class_name: str) -> str:
    data = json.loads(json_data)
    process_class(data, class_name)

    all_classes = "\n\n".join(class_definitions.values())
    return all_classes


# Sample JSON data with nested structures
json_data = """
{
  "item1": "This is a test",
  "item2": {
    "sub_item1": "foo",
    "sub_item2": "bar"
  },
  "item3": {
    "a_float_number": 1.5,
    "item4": {
      "sub_item1": 1,
      "sub_item2": 2
    }
  }
}
"""

# Generate dataclass Python code

folder_name = "python_utilities"
input_file = os.path.join(folder_name, "example.json")
read_from_input_file = True

# Generate dataclass Python code
if read_from_input_file:
    with open(input_file, "r") as file:
        data = file.read()
        python_code = generate_dataclass(str(data), "TestClass")
else:
    python_code = generate_dataclass(json_data, "TestClass")


print(python_code)
output_file = os.path.join(folder_name, "dataclass_example_result.py")


# Writing to file
with open(output_file, "w") as generated_py:
    generated_py.write("from typing import List\n")
    generated_py.write("from dataclasses import dataclass\n\n\n")
    generated_py.write(python_code)
