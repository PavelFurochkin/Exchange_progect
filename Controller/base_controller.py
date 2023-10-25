import json
from abc import ABC, abstractmethod
from http.server import BaseHTTPRequestHandler
from http.client import HTTPException
import sqlite3
from my_exception import MyError


class BaseController(ABC):
    handler: BaseHTTPRequestHandler = None

    def __init__(self, handler: BaseHTTPRequestHandler):
        self.handler = handler

    @abstractmethod
    def do_GET(self):
        pass

    @abstractmethod
    def do_POST(self):
        pass

    def do_PATCH(self):
        pass

    def send(self, code: int, data):
        json_data = json.dumps(
                    data, default=lambda x: x.__dict__,
                    indent=4, ensure_ascii=False
                )
        self.handler.send_response(code)
        self.handler.send_header('Content-Type', 'application/json')
        self.handler.end_headers()
        self.handler.wfile.write(json_data.encode('utf-8'))

    def error_handler(self, exception):
        try:
            if isinstance(exception, sqlite3.DatabaseError):
                error_message = f'возникла ошибка при работе с базой данных {exception}'
                self.send(500, {'error': error_message})
            if isinstance(exception, (ValueError, TypeError)):
                error_message = f'Такой валюты нет в базе'
                self.send(404, {'error': error_message})
            if isinstance(exception, HTTPException):
                error_message = f'Некорректный запрос'
                self.send(400, {'error': error_message})
            if isinstance(exception, IndexError):
                error_message = f'Не хватает данных для выполнения'
                self.send(400, {'error': error_message})
            if isinstance(exception, MyError):
                error_message = f'Валютная пара с таким кодом уже существует'
                self.send(409, {'error': error_message})
        except Exception as error:
            error_message = f'Возникла ошибка {error}'
            self.send(400, {'error': error_message})
