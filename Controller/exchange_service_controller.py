from Controller.base_controller import BaseController
from urllib.parse import urlparse
from Service.currencies_service import CurrenciesService


class ExchangeCurrency(BaseController):
    def __init__(self, handle):
        super().__init__(handle)
        self.handle = handle

    def do_GET(self):
        try:
            path_query = urlparse(self.handle.path.split('/')[1]).query
            path_split = path_query.split('&')
            result_dict = {}

            for item in path_split:
                key, value = item.split('=')
                result_dict[key] = value

            response = CurrenciesService().converting_currency(result_dict)
            self.send(200, response)
        except Exception as error:
            self.error_handler(error)

    def do_POST(self):
        pass

    def do_PATCH(self):
        pass
