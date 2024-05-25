from dataclasses import dataclass, field, asdict
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

    def return_result(self):
        """Функция для преобразования датаклассов - атрибутов объекта в словарь для удобства
        отправки и записи в файл"""
        result = {'original_part': asdict(self.original_parts),
                  'analog_parts': [asdict(part) for part in self.analog_parts]}
        return result


class Shop:
    def __init__(self, name, session):
        self.shop_name = name
        self.session = session


