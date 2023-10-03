from abc import ABC, abstractmethod
from http.server import BaseHTTPRequestHandler

class BaseController(ABC):
    handler: BaseHTTPRequestHandler = None

    def __init__(self, handler: BaseHTTPRequestHandler):
        self.handler = handler
        # self.handle()

    def handle(self):
        try:
            if self.handler.command == 'GET':
                self.do_GET()
            elif self.handler.command == 'POST':
                self.do_Post()
            else:
                self.handler.send_error(405, 'Метод не найден')
        except Exception as error:
            self.error_handler(error)


    @abstractmethod
    def do_GET(self):
        pass
    @abstractmethod
    def do_Post(self):
        pass

    def send(self, code: int, data):
        self.handler.send_response(code)
        self.handler.send_header('Content-Type', 'application/json; charset=UTF-8')
        self.handler.end_headers()
        self.handler.wfile.write(data.encode('utf-8'))

    def error_handler(self, exception):
        try:
            if isinstance(exception, AttributeError) :
                self.send(500, f'возникла ошибка при работе с базой данных {exception}')
        except Exception as error:
            print(f'Возникла ошибка: {error}')
