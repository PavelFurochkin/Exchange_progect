from http import HTTPStatus
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import Execute_from_db as Ex_db


class HelloWorld:
    def __init__(self, hello):
        self.hello = hello


Hello = HelloWorld('world')


class OurHandler(BaseHTTPRequestHandler):
    # Метод обрабатывает каждую валюту из таблицы
    def currencies(self):
        data = Ex_db.ExecuteBdCurrency('Exchange_base.db', 'Currencies').execute()
        currencies_list = []
        for currency in data:
            current_currency = Ex_db.Currency(*currency)
            currency_dict = {
                'id': current_currency.id,
                'name': current_currency.full_name,
                'code': current_currency.code,
                'sign': current_currency.sign
            }
            currencies_list.append(currency_dict)

        self.send_response(HTTPStatus.OK)
        self.send_header('Content-Type', 'application/json; charset=UTF-8')
        self.end_headers()

        response = json.dumps(currencies_list, indent=4, ensure_ascii=False)
        self.wfile.write(response.encode('utf-8'))

    def hello_page(self):
        self.send_response(HTTPStatus.OK)
        self.send_header('Content-Type', 'text/html; charset = UTF-8')
        self.end_headers()

        self.wfile.write('<h1>Hello World</h1>'.encode('utf-8'))

    def test_page(self):
        self.send_response(HTTPStatus.OK)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()

        json_string = json.dumps(Hello.__dict__)

        self.wfile.write(bytes(json_string, 'utf-8'))

    def do_GET(self):
        if self.path == '/hello':
            self.hello_page()
        if self.path == '/test':
            self.test_page()
        if self.path == '/currencies':
            self.currencies()


if __name__ == '__main__':
    with HTTPServer(('', 8000), OurHandler) as server:
        server.serve_forever()
