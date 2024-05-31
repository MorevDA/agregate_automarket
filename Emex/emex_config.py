from requests import Session
from requests.cookies import RequestsCookieJar


class Config:
    def __init__(self, session: Session):
        self.cookies_url: str = 'https://emex.ru'
        self.search_url: str = 'https://emex.ru/api/search/search2'
        self.params_for_search: dict = {
            'detailNum': '4451809000',
            'isHeaderSearch': 'true',
            'showAll': 'true',
            'searchSource': 'direct',
            'searchString': '4451809000',
            'locationId': '11912',  # офис выдачи, при дальнейшем развитии проекта возможно динамически изменять
        }
        self.headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
            'Access-Control-Allow-Credentials': 'true',
            'Access-Control-Allow-Origin': 'https://emex.ru',
            'Content-Type': 'application/json',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/124.0.0.0 Safari/537.36',
            'expires': '0',
            'pragma': 'no-cache',
            'sec-ch-ua': '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'traceparent': '00-1e7a20e791e3b5eecf3af3e69f85f618-d5ea45462fd2d820-01',
        }
        self.cookies = self._get_cookies(session)

    def _get_cookies(self, session) -> RequestsCookieJar:
        """Метод для получения cookies"""
        cook = session.get(url=self.cookies_url).cookies
        return cook
