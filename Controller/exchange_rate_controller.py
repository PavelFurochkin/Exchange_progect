from urllib.parse import parse_qs

from Controller.base_controller import BaseController
from DAO import CurrenciesDAO, GetFromDB


class ExchangeRate(BaseController):
    def __init__(self, handler):
        super().__init__(handler),
        self.from_dao = GetFromDB()
        self.dao = CurrenciesDAO()


    def do_GET(self):
        path = self.handler.path.split('/')[2]
        path_params = tuple((path[:3], path[3:]))
        base_currency = self.from_dao.get_currency_by_code(path_params[0]).get('id')
        target_currency = self.from_dao.get_currency_by_code(path_params[1]).get('id')
        response = self.from_dao.get_exchange_rate_by_code(base_currency, target_currency)
        self.send(200, response)
        self.dao.close()

    def do_POST(self):
        pass

    def do_PATCH(self):
        try:
            __rate = 0
            __content_type = self.handler.headers.get('Content-Type', '')
            if __content_type.strip() == 'application/x-www-form-urlencoded':
                content_length = int(self.handler.headers['content-length'])
                post_data = self.handler.rfile.read(content_length).decode('utf-8')
                form_data = parse_qs(post_data)
                __rate = float(form_data.get('rate', '')[0])

            __path = self.handler.path.split('/')[2]
            __path_params = tuple((__path[:3], __path[3:]))
            __base_currency = self.from_dao.get_currency_by_code(__path_params[0]).get('id')
            __target_currency = self.from_dao.get_currency_by_code(__path_params[1]).get('id')
            __pair_for_patch = self.from_dao.get_exchange_rate_by_code(__base_currency, __target_currency)
            __response = self.dao.update_data(__pair_for_patch.get('id'), __rate)
            __fresh_pair = self.from_dao.get_exchange_rate_by_code(__base_currency, __target_currency)
            self.send(200, __fresh_pair)
            self.dao.close()
        except Exception as error:
            self.error_handler(error)
