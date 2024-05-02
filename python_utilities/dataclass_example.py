from dataclasses import dataclass
from typing import List


@dataclass
class PropertiesClass:
    propery_one: int


@dataclass
class GeometryClass:
    type: str
    coordinates: List[float]


@dataclass
class FeaturesClass:
    type: str
    properties: PropertiesClass
    geometry: GeometryClass


@dataclass
class TestClass:
    type: str
    features: List[FeaturesClass]
