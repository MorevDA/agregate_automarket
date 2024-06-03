from requests import Session
from requests.cookies import RequestsCookieJar


class Config:
    def __init__(self, session: Session):
        self.cookies_url: str = 'https://avsila.ru/'
        self.search_url: str = 'https://avsila.ru/local/includes/ajax/_lm.json.search_result.php'
        self.params_for_search: dict = {
            'q': '4451809000',
            'brand_title': 'DS',
        }
        self.headers = {'Accept': '*/*',
                        'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
                        'Connection': 'keep-alive',
                        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                        'Origin': 'https://avsila.ru',
                        'Referer': 'https://avsila.ru/auto/search/4451809000/?brand_title=DS',
                        'Sec-Fetch-Dest': 'empty',
                        'Sec-Fetch-Mode': 'cors',
                        'Sec-Fetch-Site': 'same-origin',
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
                        'X-Requested-With': 'XMLHttpRequest',
                        'sec-ch-ua': '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
                        'sec-ch-ua-mobile': '?0',
                        'sec-ch-ua-platform': '"Windows"',
                        }
        self.cookies = self._get_cookies(session)

    def _get_cookies(self, session) -> RequestsCookieJar:
        """Метод для получения cookies"""
        cook = session.get(url=self.cookies_url).cookies
        return cook
