from Controller.base_controller import BaseController
from urllib.parse import urlparse
from DAO import CurrenciesDAO, GetFromDB


class ExchangeCurrency(BaseController):
    def __init__(self, handle):
        super().__init__(handle)
        self.handle = handle

    def do_GET(self):
        path_query = urlparse(self.handle.path.split('/')[1]).query
        path_split = path_query.split('&')
        result_dict = {}

        for item in path_split:
            key, value = item.split('=')
            result_dict[key] = value



        c=1

    def do_POST(self):
        pass

    def do_PATCH(self):
        pass