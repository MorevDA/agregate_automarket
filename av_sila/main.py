from dataclasses import dataclass

from base_app.shop_schemas import Parts_Information, Suggestion, Part


@dataclass
class AVS_Parts_Information(Parts_Information):

    def __post_init__(self):
        self.config.params_for_search['q'] = self.original_part_number
        full_json_data = self._get_full_parts_information()
        self.original_parts = self._get_parts_information(full_json_data['analog_type_N'])

    def _get_full_parts_information(self) -> dict:
        """Метод для получения полной информации(оригиналы и аналоги) по запчасти с искомым парт-номером"""
        full_part_information = self._get_content_post_method(url=self.config.search_url, headers=self.config.headers,
                                                              data=self.config.params_for_search,
                                                              cookies=self.config.cookies)

        return full_part_information['parts']

    def _get_parts_information(self, content: dict) -> Part:
        """Метод для формирования предложений по деталям с искомым пар-номером"""
        brand = list(content)[0]
        part_number = list(content[brand])[0]
        suggestion_info = content[brand][part_number]['items']
        part_name = suggestion_info[0]['title']
        original = Part(brand, part_number, part_name)
        original.suggestions = [self._get_suggestions(supply) for supply in suggestion_info]
        return original

    # def _get_analog_part_information(self, content: dict) -> list(Part):


    @staticmethod
    def _get_suggestions(part_info: dict) -> Suggestion:
        """Метод для создания экземпляра класса Suggestion из словаря"""
        delivery_time = part_info['delivery_time'].split()[0]
        return Suggestion(part_info['price'], part_info['quantity'], delivery_time, delivery_time)
