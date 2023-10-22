from Controller.base_controller import BaseController
from DAO import CurrenciesDAO, GetFromDB


class ExchangeRates(BaseController):
    def __init__(self, handler):
        super().__init__(handler),
        self.dao = CurrenciesDAO()
        self.from_dao = GetFromDB()

    def do_GET(self):
        try:
            currencies_exchange = self.from_dao.get_all_exchange_rate()
            self.send(200, currencies_exchange)
            self.dao.close()
        except Exception as error:
            self.error_handler(error)

    def do_POST(self):
        pass

