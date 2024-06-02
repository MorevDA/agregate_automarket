from dataclasses import dataclass

from base_app.shop_schemas import Parts_Information, Suggestion, Part
from va_config import Config


@dataclass
class VA_Parts_Information(Parts_Information):
    brand: str = None

    def __post_init__(self):
        """Метод для получения предложений по запрашиваемому парт-номеру (как оригинальных деталей,
        так и замениелей"""
        self.config.params_for_brand_search['article'] = self.original_part_number
        self.config.params_for_search['article'] = self.original_part_number
        self._get_brand_name()
        parts_content: dict = self._get_raw_parts_information().get('data')['rows']
        self._get_original_parts(parts_content['request'])
        self._get_analog_parts(parts_content['nonOriginalAnalog'])

    def _get_brand_name(self) -> None:
        """Метод для получения от API наименования бренда-производителя детали с искомым парт-номером"""
        content = self.session.get(self.config.search_url, params=self.config.params_for_brand_search,
                                   cookies=self.config.cookies, headers=self.config.headers)
        brand: str = content.json().get('data').get('brands')[0]['name']
        self.config.params_for_search['brand'] = brand
        self.brand = brand

    def _get_original_parts(self, input_data: list) -> None:
        self.original_parts = Part(input_data[0]['brand'], input_data[0]['articleDisplay'], input_data[0]['name'], '')
        self.original_parts.suggestions = list(map(self.get_suggestion, input_data))

    def _get_analog_parts(self, analog_json: list) -> None:
        """Метод для получения перечня возможных замен для искомого парт-номера"""
        analog_json.sort(key=lambda x: x['brand'])
        part_brand = Part(analog_json[0]['brand'], analog_json[0]['articleDisplay'], analog_json[0]['name'])
        analog_parts = []
        for part_data in analog_json:
            if part_data['brand'] == part_brand.brand and part_data['articleDisplay'] == part_brand.part_number:
                part_brand.suggestions.append(self.get_suggestion(part_data))
            else:
                analog_parts.append(part_brand)
                part_brand = Part(part_data['brand'], part_data['articleDisplay'], part_data['name'])
                part_brand.suggestions.append(self.get_suggestion(part_data))
        self.analog_parts = analog_parts

    @staticmethod
    def get_suggestion(part: dict) -> Suggestion:
        """Метод для преобразования json-объекта в экземпляр класса Suggestion"""
        suggestion = Suggestion(part['price'], part['amountNum'], part['term'], part['termMax'])
        return suggestion
