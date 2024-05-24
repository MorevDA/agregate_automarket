from dataclasses import dataclass, field
from requests import Session


@dataclass
class Suggestion:
    price: float
    value: int
    min_delivery_time: int
    max_delivery_time: int


@dataclass
class Part:
    brand: str
    part_number: str
    name: str
    art_id: str
    suggestions: list[Suggestion] = field(default_factory=list)


@dataclass
class Parts_Information:
    session: Session
    shop_name: str = None
    original_parts: Part = None
    analog_parts: list[Part] = field(default_factory=list)



class Shop:
    def __init__(self, name, session):
        self.shop_name = name
        self.session = session


