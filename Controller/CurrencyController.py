import json
from http.client import HTTPException

from Controller.BaseController import BaseController
from DAO.DAO import CurrenciesDAO

class CurrencyController(BaseController):
    def __init__(self, handler):
        self.dao = CurrenciesDAO()
        super().__init__(handler)

    def do_GET(self):
        try:
            code = self.handler.path.split('/')[-1]
            if code == '':
                raise HTTPException
            currency = self.dao.get_currency_by_code(code)

            self.send(200, currency)
        except Exception as error:
            self.error_handler(error)
        finally:
            self.dao.close()

    def do_POST(self):
        pass