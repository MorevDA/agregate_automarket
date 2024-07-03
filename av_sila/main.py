from dataclasses import dataclass

from base_app.shop_schemas import Parts_Information, Suggestion, Part


@dataclass
class AVS_Parts_Information(Parts_Information):

    def __post_init__(self):
        self.config.params_for_search['q'] = self.original_part_number
        self._get_brand_name()
        full_json_data = self._get_full_parts_information()
        self.original_parts = self._get_original_part(full_json_data['analog_type_N'])
        self.analog_parts = self._get_analog_part_information(full_json_data['analog_type_0'])

    def _get_brand_name(self) -> None:
        """Метод для получения имени бренда-производителя детали с запрашиваемым парт-номером"""
        data = self._get_content_post_method(url=self.config.search_url, headers=self.config.headers,
                                                              data=self.config.params_for_search,
                                                              cookies=self.config.cookies)
        self.config.params_for_search['brand_title'] = list(data['catalogs'])[0]

    def _get_full_parts_information(self) -> dict:
        """Метод для получения полной информации(оригиналы и аналоги) по запчасти с искомым парт-номером"""
        full_part_information = self._get_content_post_method(url=self.config.search_url, headers=self.config.headers,
                                                              data=self.config.params_for_search,
                                                              cookies=self.config.cookies)

        return full_part_information['parts']

    def _get_parts_information(self, content: dict) -> Part:
        """Метод для формирования предложений по деталям с искомым пар-номером"""
        part_number = list(content)[0]
        suggestion_info = content[part_number]['items']
        part_name = suggestion_info[0]['title']
        brand = suggestion_info[0]['brand_title']
        original = Part(brand, part_number, part_name)
        original.suggestions = [self._get_suggestions(supply) for supply in suggestion_info]
        return original

    def _get_original_part(self, data: dict) -> Part:
        brand = list(data.keys())[0]
        return self._get_parts_information(data[brand])

    def _get_analog_part_information(self, content: dict) -> list[Part]:
        """Метод для получения перечня аналогов запчасти с искомым парт-номером"""
        all_brands: list = list(content.keys())
        all_analog_information = [self._get_parts_information(content[brand]) for brand in all_brands]
        return all_analog_information



    @staticmethod
    def _get_suggestions(part_info: dict) -> Suggestion:
        """Метод для создания экземпляра класса Suggestion из словаря"""
        delivery_time = part_info['delivery_time'].split()[0]
        return Suggestion(part_info['price'], part_info['quantity'], delivery_time, delivery_time)
