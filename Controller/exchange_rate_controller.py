from Controller.base_controller import BaseController
from DAO.DAO import CurrenciesDAO


class ExchangeRate(BaseController):
    def __init__(self, handler):
        super().__init__(handler),
        self.dao = CurrenciesDAO()

    def do_GET(self):
        path = self.handler.path.split('/')[2]
        path_params = tuple((path[:3], path[3:]))
        base_currency = self.dao.get_currency_by_code(path_params[0]).get('id')
        target_currency = self.dao.get_currency_by_code(path_params[1]).get('id')
        response = self.dao.get_exchange_rate_by_code(base_currency, target_currency)
        self.send(200, response)
        self.dao.close()

    def do_POST(self):
        pass

    def do_PATCH(self):
        pass