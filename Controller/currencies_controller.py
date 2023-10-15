import json
import sqlite3
from urllib.parse import parse_qs
from http.client import HTTPException

from Controller.base_controller import BaseController
from DAO.DAO import CurrenciesDAO


class CurrenciesController(BaseController):
    def __init__(self, handler):
        super().__init__(handler)

        self.dao = CurrenciesDAO()

    def do_GET(self):
        try:
            currencies = self.dao.get_all_currencies()
            self.send(200, currencies)
            self.dao.close()
        except Exception as error:
            self.error_handler(error)



    def do_POST(self):
        try:
            content_type = self.handler.headers.get('Content-Type', '')
            if content_type.strip() == 'application/x-www-form-urlencoded':
                content_length = int(self.handler.headers['content-length'])
                post_data = self.handler.rfile.read(content_length).decode('utf-8')
                form_data = parse_qs(post_data)
                code = form_data.get('code','')[0]
                name = form_data.get('name','')[0]
                sing = form_data.get('sign','')[0]
                if self.dao.check_code(code):
                    error = 'Такая валюта уже есть в базе'
                    self.send(400, {'error': error})
                    return
                else:
                    self.dao.add_currency(code, name, sing)
                    currency_code = self.dao.get_currency_by_code(code)
                    self.send(200, currency_code)
            else:
                raise HTTPException
        except Exception as error:
            self.error_handler(error)
        finally:
            self.dao.close()
