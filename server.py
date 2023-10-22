from http.server import HTTPServer, BaseHTTPRequestHandler

from Controller.base_controller import BaseController
from Router.router import PathRouter


class OurHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        controller: BaseController = self.initiate_controller()
        controller.do_GET()

    def do_POST(self):
        controller: BaseController = self.initiate_controller()
        controller.do_POST()

    def do_PATCH(self):
        controller: BaseController = self.initiate_controller()
        controller.do_PATCH()

    def initiate_controller(self):
        """ Метод возвращает контроллер в зависимости от пути"""
        try:
            controller_class = PathRouter.determine_controller_class_by_path(self.path)
            return controller_class(self)
        except Exception as error:
            return self.send_error(404, str(''))


if __name__ == '__main__':
    with HTTPServer(('', 8000), OurHandler) as server:
        server.serve_forever()
