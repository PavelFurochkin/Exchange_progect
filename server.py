import sqlite3
from http.server import HTTPServer, BaseHTTPRequestHandler

from Controller.BaseController import BaseController
from Router.Router import PathRouter
from DAO.DAO import CurrenciesDAO


class OurHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        controller: BaseController = self.initiate_controller()
        try:
            controller.do_GET()
        except sqlite3.Error as error:
            print(f'Возникла ошибка {error}')

    def initiate_controller(self):
        """ Метод возвращает контроллер в зависимости от пути"""
        try:
            controller_class = PathRouter.determine_controller_class_by_path(self.path)
            return controller_class(self)
        except Exception as error:
            self.send_error(404, str(''))


if __name__ == '__main__':
    with HTTPServer(('', 8000), OurHandler) as server:
        server.serve_forever()
