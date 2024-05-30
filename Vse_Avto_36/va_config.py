from requests import Session
from requests.cookies import RequestsCookieJar


class Config:
    def __init__(self, session):
        self.cookies_url: str = 'https://www.va36.ru'
        self.search_url: str = 'https://www.va36.ru/api/v2/client/fast-search/'
        self.params_for_brand_search: dict = {'article': "", 'withAnalogs': '1'}
        self.params_for_search = {'article': None, 'brand': None, 'withAnalogs': '1'}
        self.headers = {'authority': 'www.va36.ru',
                        'accept': '*/*',
                        'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
                        'referer': 'https://www.va36.ru/',
                        'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
                        'sec-ch-ua-mobile': '?0',
                        'sec-ch-ua-platform': '"Windows"',
                        'sec-fetch-dest': 'empty',
                        'sec-fetch-mode': 'cors',
                        'sec-fetch-site': 'same-origin',
                        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
                        'warlng': 'undefined',
                        }
        self.session: Session = session
        self.cookies = self._get_cookies()

    def _get_cookies(self) -> RequestsCookieJar:
        """Метод для получения cookies"""
        cookies = self.session.get(self.cookies_url, headers=self.headers).cookies
        return cookies
