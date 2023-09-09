from http import HTTPStatus
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from Router.Router import PathRouter
from DAO.DAO import CurrenciesDAO


class OurHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.command == 'GET':
            data = self.get_data()
            self.response(data)

        else:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b'Bad Request')

    def get_data(self):
        """ Метод возвращает определенную страницу в зависимоти от пути"""
        path: str = PathRouter.determine_path(self.path)
        if path[-1] == '/':
            path_detail: tuple = PathRouter.determine_path_params(self.path)
            data: tuple = CurrenciesDAO('Exchange_base.db').get_currency_by_code(path_detail[0])
            response: str = json.dumps(data, indent=4, ensure_ascii=False)
            return response
        else:
            data: list = CurrenciesDAO('Exchange_base.db').get_all_currencies()
            response: str = json.dumps(
                     data, default=lambda x: x.__dict__,
                     indent=4, ensure_ascii=False
                 )
            return response

    def response(self, data):

        self.send_response(200)
        self.send_header('Content-Type', 'application/json; charset=UTF-8')
        self.end_headers()
        self.wfile.write(data.encode('utf-8'))


if __name__ == '__main__':
    with HTTPServer(('', 8000), OurHandler) as server:
        server.serve_forever()

