import json
import os
import textwrap

import numpy as np
from typing_extensions import LiteralString


class my_prettier(json.JSONEncoder):
    width = 100

    # BUG incompatible overriding
    def iterencode(self, o, _one_shot: bool = False):  # -> LiteralString: # Iterator[str]
        if self.ensure_ascii:
            str_encoder = json.encoder.encode_basestring_ascii
        else:
            str_encoder = json.encoder.encode_basestring

        def floatstr(o, allow_nan=self.allow_nan):
            if o != o:
                text = "NaN"
            elif o == json.encoder.INFINITY:
                text = "Infinity"
            elif o == -json.encoder.INFINITY:
                text = "-Infinity"
            else:
                return float.__repr__(o)

            if not allow_nan:
                raise ValueError("Out of range float values are not JSON compliant: " + repr(o))

            return text

        def parse_object(o, current_indent_level, indent, item_separator, key_separator, offset):
            if isinstance(o, str):
                return str_encoder(o)
            elif o is None:
                return "null"
            elif o is True:
                return "true"
            elif o is False:
                return "false"
            elif isinstance(o, int):
                return int.__repr__(o)
            elif isinstance(o, float):
                return floatstr(o)
            elif isinstance(o, (list, tuple)):
                return parse_list(o, current_indent_level + 1, indent, item_separator, key_separator, offset)
            elif isinstance(o, dict):
                return parse_dict(o, current_indent_level + 1, indent, item_separator, key_separator, offset)
            elif isinstance(o, np.ndarray):
                return parse_list(o.tolist(), current_indent_level + 1, indent, item_separator, key_separator, offset)
            elif isinstance(o, np.integer):
                return int.__repr__(int(o))
            else:
                return super().default(o)

        def parse_list(lst, current_indent_level, indent, item_separator, key_separator, offset):
            if not lst or len(lst) == 0:
                return "[]"

            elements_indent = None
            root_indent = None
            if indent is not None:
                elements_indent = indent * current_indent_level
                root_indent = indent * (current_indent_level)

            parsed_buf = ""
            elem = ""
            sub_elements = []
            sub_elements_len = 0
            last_elem = len(lst) - 1
            same_line = True

            for index, value in enumerate(lst):
                elem = parse_object(
                    value, current_indent_level, indent, item_separator, key_separator, offset + len("[]")
                )
                sub_elements.append(elem)

                if "\n" in elem:
                    same_line = False
                sub_elements_len += len(elem)
                if last_elem != elem:
                    sub_elements_len += len(item_separator)

            if same_line:
                if offset + sub_elements_len < self.width + 1:
                    parsed_buf = item_separator.join(sub_elements)
                else:
                    all_numbers = all([isinstance(e, (int, float)) for e in lst])
                    assert elements_indent is not None
                    if len(elements_indent) + sub_elements_len < self.width + 1:
                        parsed_buf = "\n" + elements_indent
                        if all_numbers:
                            parsed_buf += item_separator.join(sub_elements)
                        else:
                            parsed_buf += (item_separator + "\n" + elements_indent).join(sub_elements)
                    else:
                        parsed_buf = "\n" + elements_indent
                        if all_numbers:
                            wraped_str = textwrap.TextWrapper(width=(self.width - len(elements_indent))).wrap(
                                item_separator.join(sub_elements)
                            )
                            parsed_buf += ("\n" + elements_indent).join(wraped_str)
                        else:
                            parsed_buf += (item_separator + "\n" + elements_indent).join(sub_elements)
                    assert root_indent is not None
                    parsed_buf += "\n" + root_indent
            if not same_line:
                assert elements_indent is not None
                parsed_buf = "\n" + elements_indent
                parsed_buf += (item_separator + "\n" + elements_indent).join(sub_elements)
                assert root_indent is not None
                parsed_buf += "\n" + root_indent

            parsed_buf = "[" + parsed_buf + "]"

            return parsed_buf

        def parse_dict(dct, current_indent_level, indent, item_separator, key_separator, offset):
            if not dct:
                return "{}"

            newline_indent = None
            current_indent = None

            if indent is not None:
                current_indent = indent * current_indent_level
                newline_indent = "\n" + current_indent

            parsed_buf = ""
            elem = ""
            key_elem = ""

            for key, value in dct.items():
                if isinstance(key, str):
                    pass
                elif isinstance(key, (float, int)) or key is True or key is False or key is None:
                    key = parse_object(key, current_indent_level, indent, item_separator, key_separator, offset)
                else:
                    raise TypeError("keys must be str, int, float, bool or None, not {key.__class__.__name__}")
                assert current_indent is not None
                key_elem = current_indent + str_encoder(key) + key_separator
                parsed_buf += (
                    "\n"
                    + key_elem
                    + parse_object(value, current_indent_level, indent, item_separator, key_separator, len(key_elem))
                )
                parsed_buf += item_separator
            parsed_buf = parsed_buf[: -len(item_separator)]
            assert newline_indent is not None
            return "{" + parsed_buf + newline_indent[: -len(indent)] + "}"

        def post_parse(buf):
            lines = buf.split("\n")
            stripped_lines = [line.rstrip() for line in lines]
            return "\n".join(stripped_lines)

        if self.indent is not None and not isinstance(self.indent, str):
            self.indent = " " * self.indent

        parsed_object = parse_object(o, 0, self.indent, self.item_separator, self.key_separator, 0)
        return post_parse(parsed_object + "\n")


def main():
    folder_name = "python_utilities"
    json_output_name = "output_example.json"
    json_input_filename = "example.json"
    json_input = os.path.join(folder_name, json_input_filename)
    json_output = os.path.join(folder_name, json_output_name)

    with open(json_input, "r") as input_json:
        obj = json.load(input_json)
        with open(json_output, "w") as output_json:
            json.dump(obj, output_json, indent=2, separators=(", ", ": "), cls=my_prettier)


if __name__ == "__main__":
    main()
