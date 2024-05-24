class Config:
    """Класс для хранения параметров поисковых запросов"""

    def __init__(self, session):
        self.headers_auth: dict = {'accept': 'application/json, text/plain, */*',
                                   'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
                                   'origin': 'https://armtek.ru',
                                   'referer': 'https://armtek.ru/',
                                   'sec-ch-ua': '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
                                   'sec-ch-ua-mobile': '?0',
                                   'sec-ch-ua-platform': '"Windows"',
                                   'sec-fetch-dest': 'empty',
                                   'sec-fetch-mode': 'cors',
                                   'sec-fetch-site': 'same-site',
                                   'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, '
                                                 'like Gecko) Chrome/123.0.0.0 Safari/537.36',
                                   'x-auth-system': 'AUTH_MICROSERVICE_V1_ARMTEK_RU',
                                   'x-auth-token': 'nJhNK87gJOOU6dfr',
                                   'x-ca-vkorg': '4000',
                                   }

        self.headers_search: dict = {'accept': 'application/json, text/plain, */*',
                                     'accept-language': 'ru,en;q=0.9,en-GB;q=0.8,en-US;q=0.7',
                                     'content-type': 'application/json',
                                     'origin': 'https://armtek.ru',
                                     'referer': 'https://armtek.ru/',
                                     'sec-ch-ua': '"Microsoft Edge";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
                                     'sec-ch-ua-mobile': '?0',
                                     'sec-ch-ua-platform': '"Windows"',
                                     'sec-fetch-dest': 'empty',
                                     'sec-fetch-mode': 'cors',
                                     'sec-fetch-site': 'same-site',
                                     'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 ('
                                                   'KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.0.0',
                                     'x-app-version': '1.5.2205',
                                     'x-ca-vkorg': '4000',
                                     }
        self.art_id_data: dict = {'query': "",
                                  'queryType': 1,
                                  'page': 1,
                                  'filters': {
                                      'text': ''
                                  },
                                  'userInfo': {
                                      'VKORG': '4000',
                                      'VSTELS_LIST': [
                                          'PE90',
                                      ],
                                  },
                                  'ZZSIGN': 'S', }
        self.related_parts_search_data: dict = {'query': None, 'queryType': 1, 'page': 1, 'artId': None,
                                                'typeView': 'list', 'filters': {'text': None, 'artId': None,
                                                                                },
                                                'userInfo': {'VKORG': '4000', 'VSTELS_LIST': ['PE90', ], },
                                                'ZZSIGN': 'S'}
        self.final_search_data = {'artId': 49207054, 'userInfo': {'VKORG': '4000', 'VSTELS_LIST': ['PE90',]},
                                  'limitSuggestions': False, }

        self.token_url: str = 'https://restapi.armtek.ru/rest/ru/auth-microservice/v1/guest'
        self.final_search_url: str = 'https://restapi.armtek.ru/rest/ru/search-microservice/v1/search/all-suggestions'
        self.art_id_url: str = 'https://restapi.armtek.ru/rest/ru/search-microservice/v1/search'
        self.analog_url: str = 'https://restapi.armtek.ru/rest/ru/search-microservice/v1/search/by-related'
        self.get_token(session)

    def get_token(self, session):
        """Метод для получения jwt-токена для работы с API."""
        response_result = session.post(self.token_url, headers=self.headers_auth, json={})
        token_data = response_result.json()['data']['accessToken']
        authorization_token = f'Bearer {token_data}'
        self.headers_search['authorization'] = authorization_token
