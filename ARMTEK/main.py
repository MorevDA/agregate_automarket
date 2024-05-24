from dataclasses import dataclass, asdict
from copy import deepcopy
from datetime import date

from armtek_config import Config
from shop_schemas import Parts_Information, Part, Suggestion


@dataclass
class Armtek_Parts_Information(Parts_Information):
    original_part_number: str = None
    config: Config = None

    def __post_init__(self):
        self.__get_art_id()
        all_detail = self.__get_parts_with_suggestions()
        self.original_parts = all_detail.pop(0)
        self.analog_parts = all_detail

    def __get_art_id(self) -> None:
        """Функция для получения от API Armtek внутреннего артикула Armtek для дальнейшего поиска в базе Armtek"""
        self.config.art_id_data['query'] = (
            self.config.art_id_data)['filters']['text'] = self.config.related_parts_search_data['query'] \
            = self.config.related_parts_search_data['filters']['text'] = self.original_part_number
        self.config.art_id_data['filters']['text'] = self.original_part_number
        content = self.__get_content_post_method(self.session, self.config.art_id_url, self.config.headers_search,
                                                 self.config.art_id_data)
        parts_data = content["data"]['articlesData'][0]
        art_id = parts_data['ARTID']
        self.config.related_parts_search_data['artId'] = art_id
        self.config.related_parts_search_data['filters']['artId'] = art_id

    def __get_pages_count(self) -> int:
        """Функция для получения количества страниц с предложениями о деталях"""
        response = self.__get_content_post_method(self.session, self.config.art_id_url, self.config.headers_search,
                                                  self.config.related_parts_search_data)

        return response['data']['pagination']['pageCount']

    def __get_part_on_page(self, search_data: dict) -> list[Part]:
        """Функция для получения основной информации о деталях с одной страницы"""
        self.config.headers_search['authority'] = 'restapi.armtek.ru'
        content = self.__get_content_post_method(self.session, self.config.art_id_url, self.config.headers_search,
                                                 search_data)
        return self.get_part_info(content, Part)

    def __get_parts_on_all_pages(self) -> list[Part]:
        """Функция для получения основной информации о деталях с искомым парт-номером"""
        pages_count = self.__get_pages_count()
        all_parts = []
        for page_number in range(1, pages_count + 1):
            conf = deepcopy(self.config.related_parts_search_data)
            conf['page'] = page_number
            all_parts.extend(self.__get_part_on_page(conf))
        return all_parts

    def __get_parts_with_suggestions(self) -> list:
        """Функция для получения информации о цене и сроках поставки всех аналогов парт-номера."""
        all_parts = self.__get_parts_on_all_pages()
        for part in all_parts:
            json_data = deepcopy(self.config.final_search_data)
            json_data['artId'] = part.art_id
            content = \
                self.__get_content_post_method(self.session, self.config.final_search_url, self.config.headers_search,
                                               json_data)['data']
            suggestions_list = self.get_suggestion_list(content)
            part.suggestions = suggestions_list
        return all_parts

    def return_result(self):
        """Функция для преобразования датаклассов - атрибутов объекта в словарь для удобства
        отправки и записи в файл"""
        result = {'original_part': asdict(self.original_parts),
                  'analog_parts': [asdict(part) for part in self.analog_parts]}
        return result

    @staticmethod
    def get_part_info(json_data, part):
        """Функция для получения основных параметров аналогов оригинального артикула:
        фирма-производитель, каталожный номер производителя, наименование детали, внутренний артикул Armtek -
        для дальнейшего поиска ценовых предложений"""
        part_info_list: list = []
        for part_info in json_data['data']['articlesData']:
            part_info_list.append(part(part_info['BRAND'], part_info['PIN'], part_info['NAME'], part_info['ARTID']))
        return part_info_list

    @staticmethod
    def __get_current_time(raw_string_date: str) -> str | int:
        """Функция для вычисления времени доставки"""
        if len(raw_string_date) < 8:
            return 'n/d'
        raw_date = f'{raw_string_date[:4]}-{raw_string_date[4:6]}-{raw_string_date[6:8]}'
        current_date = date.fromisoformat(raw_date)
        delta_days = (current_date - date.today()).days
        return delta_days

    @staticmethod
    def __get_content_post_method(sess, url: str, headers: dict, json_data: dict) -> dict:
        """Функция для запроса данных от API методом POST"""
        content = sess.post(url, headers=headers, json=json_data).json()
        return content

    def get_suggestion_list(self, content: list) -> list:
        """Функция для формирования списка всех предложений по искомой детали с информацией о цене, количестве
        доступном для заказа, максимальной и минимальной дат поставки"""
        suggestion_list = [
            Suggestion(float(supply['PRICES1']), supply['RVALUE'], self.__get_current_time(supply['DLVDT']),
                       self.__get_current_time(supply['WRNTDT'])) for supply in content]
        return suggestion_list
