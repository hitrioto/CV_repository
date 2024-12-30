"""Example classes here."""

from dataclasses import dataclass


@dataclass
class PropertiesClass:
    propery_one: int


@dataclass
class GeometryClass:
    type: str
    coordinates: list[float]


@dataclass
class FeaturesClass:
    type: str
    properties: PropertiesClass
    geometry: GeometryClass


@dataclass
class TestClass:
    type: str
    features: list[FeaturesClass]
