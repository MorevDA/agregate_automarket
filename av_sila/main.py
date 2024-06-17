from dataclasses import dataclass

from base_app.shop_schemas import Parts_Information, Suggestion, Part


@dataclass
class AVS_Parts_Information(Parts_Information):

    def __post_init__(self):
        self.config.params_for_search['q'] = self.original_part_number
        self._get_brand()
        # full_parts_data = self._get_raw_parts_information()

    def _get_brand(self):
        """Метод для получения бренда производителя детали с запрашиваемым парт-номером для дальнейшего поиска
        предложений"""
        json_data = self._get_content_post_method(url=self.config.search_url, headers=self.config.headers,
                                                  data=self.config.params_for_search)
        self.config.params_for_search['brand_title'] = list(json_data['catalogs'].keys())[0]

    def _get_full_parts_information(self):
        """Метод для получения полной информации(оригиналы и аналоги) по запчасти с искомым парт-номером"""
        full_part_information = self._get_content_post_method(url=self.config.search_url, headers=self.config.headers,
                                                              data=self.config.params_for_search, cookies=self.config.cookies)

        return full_part_information
    # _get_content_post_method
