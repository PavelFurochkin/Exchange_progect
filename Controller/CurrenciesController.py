import json
import sqlite3

from Controller.BaseController import BaseController
from DAO.DAO import CurrenciesDAO

class CurrenciesController(BaseController):
    def __init__(self, handler):
        super().__init__(handler)

        self.dao = CurrenciesDAO()

    def do_GET(self):
        currencies = self.dao.get_all_currencies()
        self.send(
            200,
            json.dumps(
                currencies,
                indent=4,
                default=lambda x: x.__dict__,
                ensure_ascii=False
            )
        )



    def do_Post(self):
        pass