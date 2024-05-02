from dataclasses import dataclass
from typing import List


@dataclass
class Item2Class:
    sub_item1: str

    sub_item2: str


@dataclass
class Item4Class:
    sub_item1: int

    sub_item2: int


@dataclass
class Item3Class:
    a_float_number: float

    item4: Item4Class


@dataclass
class TestClass:
    item1: str

    item2: Item2Class

    item3: Item3Class
