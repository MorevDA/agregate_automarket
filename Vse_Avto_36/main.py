from dataclasses import dataclass

from base_app.shop_schemas import Parts_Information
from va_config import Config


@dataclass
class VA_Parts_Information(Parts_Information):
    config: Config = None
    brand: str = None

    def __post_init__(self):
        self.config.params_for_brand_search['article'] = self.original_part_number
        self.config.params_for_full_search['article'] = self.original_part_number
        self._get_brand_name()

    def _get_brand_name(self) -> None:
        """Метод для получения от API наименования бренда-производителя детали с искомым парт-номером"""
        content = self.session.get(self.config.base_search_url, params=self.config.params_for_brand_search,
                                   cookies=self.config.cookies, headers=self.config.headers)
        brand: str = content.json().get('data').get('brands')[0]['name']
        self.config.params_for_full_search['brand'] = brand
        self.brand = brand

    def _get_full_part_information(self) -> dict:
        """Метод для получения от API полного перечня деталей по запрашиваемому парт-номеру.
        Получаем json с полным перечнем предложений по искомому парт-номеру, а также возможные аналоги."""
        data = self.session.get(self.config.base_search_url, params=self.config.params_for_full_search,
                                cookies=self.config.cookies, headers=self.config.headers)
        return data.json()
