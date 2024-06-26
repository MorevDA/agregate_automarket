from dataclasses import dataclass

from base_app.shop_schemas import Parts_Information, Suggestion, Part


@dataclass
class AVS_Parts_Information(Parts_Information):

    def __post_init__(self):
        self.config.params_for_search['q'] = self.original_part_number
        full_json_data = self._get_full_parts_information()['parts']
        self.original_parts = self._get_information_original_parts(full_json_data)

    def _get_full_parts_information(self) -> dict:
        """Метод для получения полной информации(оригиналы и аналоги) по запчасти с искомым парт-номером"""
        full_part_information = self._get_content_post_method(url=self.config.search_url, headers=self.config.headers,
                                                              data=self.config.params_for_search,
                                                              cookies=self.config.cookies)

        return full_part_information

    def _get_information_original_parts(self, content: dict) -> Part:
        """Метод для формирования предложений по деталям с искомым пар-номером"""
        brand = self.config.params_for_search['brand_title']
        part_number = self.config.params_for_search['q']
        suggestion_info = content['analog_type_N'][brand][part_number]['items']
        brand_name = suggestion_info[0]['title']
        original = Part(brand, part_number, brand_name)
        original.suggestions = [self._get_suggestions(supply) for supply in suggestion_info]
        return original

    # def _get_analog_part_information(self, content: dict) -> list(Part):


    @staticmethod
    def _get_suggestions(part_info: dict) -> Suggestion:
        """Метод для создания экземпляра класса Suggestion из словаря"""
        delivery_time = part_info['delivery_time'].split()[0]
        return Suggestion(part_info['price'], part_info['quantity'], delivery_time, delivery_time)
