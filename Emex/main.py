from requests import Session
from dataclasses import dataclass

from base_app.shop_schemas import Parts_Information, Suggestion, Part


@dataclass
class Emex_Parts_Information(Parts_Information):

    def __post_init__(self):
        self.config.params_for_search['detailNum'] = self.config.params_for_search['searchString']\
            = self.original_part_number
        full_parts_data = self._get_raw_parts_information()
        self.original_parts = self.get_full_part_data(full_parts_data['searchResult']['originals'][0])
        self.analog_parts = [self.get_full_part_data(analog) for analog in full_parts_data['searchResult']['analogs']]

    def get_full_part_data(self, part_ifo: dict) -> Part:
        """Метод для получения информации по запчасти с искомым парт-номером"""
        original_part = Part(part_ifo['make'], part_ifo['detailNum'], part_ifo['name'])
        original_part.suggestions = [self.get_suggestion(offer) for offer in part_ifo['offers']]

        return original_part

    @staticmethod
    def get_suggestion(data: dict) -> Suggestion:
        """Метод для создания экземпляра класса Suggestion из данных полученных от API emex.ru"""
        return Suggestion(data['displayPrice']['value'], data['quantity'],
                          data['delivery']['value'], data['delivery']['value'])
