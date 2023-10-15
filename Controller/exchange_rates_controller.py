from Controller.base_controller import BaseController
from DAO.DAO import CurrenciesDAO


class ExchangeRates(BaseController):
    def __init__(self, handler):
        super().__init__(handler),
        self.dao = CurrenciesDAO()

    def do_GET(self):
        try:
            currencies_exchange = self.dao.get_all_exchange_rate()
            self.send(200, currencies_exchange)
            self.dao.close()
        except Exception as error:
            self.error_handler(error)

    def do_POST(self):
        pass

