from dataclasses import dataclass, field, asdict
from requests import Session
from requests.cookies import RequestsCookieJar


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
    suggestions: list[Suggestion] = field(default_factory=list)


@dataclass
class Parts_Information:
    session: Session
    shop_name: str = None
    original_parts: Part = None
    analog_parts: list[Part] = field(default_factory=list)
    original_part_number: str = None
    config: object = None

    def return_result(self):
        """Функция для преобразования датаклассов - атрибутов объекта в словарь для удобства
        отправки и записи в файл"""
        result = {'original_part': asdict(self.original_parts),
                  'analog_parts': [asdict(part) for part in self.analog_parts]}
        return result

    def _get_raw_parts_information(self) -> dict:
        """Метод для получения от API полного перечня деталей по запрашиваемому парт-номеру.
        Получаем json с полным перечнем предложений по искомому парт-номеру, а также возможные аналоги."""
        data = self.session.get(self.config.search_url, params=self.config.params_for_search,
                                cookies=self.config.cookies, headers=self.config.headers)
        return data.json()

    def _get_content_by_get_method(self, url: str, headers: dict, cookies: dict| RequestsCookieJar, param: dict) -> dict:
        """Метод для отправки запросов методом get"""
        json_data = self.session.get(url=url, headers=headers, cookies=cookies, params= param).json()
        return json_data


class Shop:
    def __init__(self, name, session):
        self.shop_name = name
        self.session = session


