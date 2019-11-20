import requests
from src.add_parsers import EmlsParamsGetter
from settings import LOGIN, PASSWORD

class EmlsRequester:
    """Class for placing adds."""
    url_login = 'https://www.emls.ru/cabinet/login/'
    url = 'https://www.emls.ru/'

    # url = 'https://www.google.com/'

    def __init__(self, login=LOGIN, password=PASSWORD):
        """
        Args:
            login (str): Login on emls.ru
            password (str): Password on emls.ru
        """

        self.login = login
        self.password = password
        self.session = self.get_session()

    def get_session(self):
        """ Create and return session on emls.ru."""

        session = requests.session()
        headers = {
            'origin': 'https://www.emls.ru',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'upgrade-insecure-requests': '1',
            'user-agent': ('Mozilla/5.0 (Macintosh;'
                           ' Intel Mac OS X 10_15_1) AppleWebKit/537.36 '
                           '(KHTML, like Gecko) Chrome/78.0.3904.97'
                           ' Safari/537.36')
        }
        session.headers.update(headers)
        login_data = {
            'login': self.login,
            'pass': self.password,
            'submit_form_auth': 1
        }
        session.post(self.__class__.url_login,
                     data=login_data)
        # print(resp.status_code)
        return session

    def post_add(self, row):
        """Post add using row from dataframe. row: pandas.Series

        Args:
            row (pandas.Series): Series from dataframe with information, that
                you want to post
        """

        self.session.post()
        # TODO: сделать нормальное выделение data
        # data = row

        return True
