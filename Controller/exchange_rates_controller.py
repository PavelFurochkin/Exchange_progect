from http.client import HTTPException

from Controller.base_controller import BaseController
from DAO import CurrenciesDAO, GetFromDB, AddIntoDB
from urllib.parse import parse_qs


class ExchangeRates(BaseController):
    def __init__(self, handler):
        super().__init__(handler),
        self.dao = CurrenciesDAO()
        self.from_dao = GetFromDB()
        self.add_in_dao = AddIntoDB()

    def do_GET(self):
        try:
            currencies_exchange = self.from_dao.get_all_exchange_rate()
            self.send(200, currencies_exchange)
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
                base_currency_code = form_data.get('baseCurrencyCode', '')[0]
                target_currency_code = form_data.get('targetCurrencyCode', '')[0]
                rate = float(form_data.get('rate', '')[0])
                self.add_in_dao.add_exchange_course(base_currency_code, target_currency_code, rate)
                added_exchange_rate = self.from_dao.get_exchange_rate_by_code(
                    base_currency_code, target_currency_code)
                self.send(200, added_exchange_rate)
            else:
                raise HTTPException
        except Exception as error:
            self.error_handler(error)
        finally:
            self.dao.close()

