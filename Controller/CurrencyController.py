import json

from Controller.BaseController import BaseController
from DAO.DAO import CurrenciesDAO

class CurrencyController(BaseController):
    def __init__(self, handler):
        super().__init__(handler)
        self.dao = CurrenciesDAO()

    def do_GET(self):
        code = self.handler.path.split('/')[-1]
        currency = self.dao.get_currency_by_code(code)

        self.send(
            200,
            json.dumps(
                currency, default=lambda x: x.__dict__,
                indent=4, ensure_ascii=False
            )
        )

    def do_Post(self):
        pass

