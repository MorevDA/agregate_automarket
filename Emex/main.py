from requests import Session
from dataclasses import dataclass

from base_app.shop_schemas import Parts_Information, Suggestion, Part


@dataclass
class Emex_Parts_Information(Parts_Information):

    def __post_init__(self):
        self.config.params_for_search['detailNum'] = self.config.params_for_search['searchString']\
            = self.original_part_number

    @staticmethod
    def get_suggestion(data: dict) -> Suggestion:
        """Метод для создания экземпляра класса Suggestion из данных полученных от API emex.ru"""
        return Suggestion(data['displayPrice']['value'], data['quantity'],
                          data['delivery']['value'], data['delivery']['value'])