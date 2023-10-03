from urllib.parse import urlparse

from Controller.CurrenciesController import CurrenciesController
from Controller.CurrencyController import CurrencyController

routes = {
    'currencies': CurrenciesController,
    'currency': CurrencyController
}

class PathRouter:
    @staticmethod
    def determine_controller_class_by_path(request_path: str):
        """ Медод позволяет получить путь"""
        path = urlparse(request_path).path
        split_path = path.split('/')
        if len(split_path) >= 2:
            route = split_path[1]
        else:
            route = '/'

        return routes.get(route)

    @staticmethod
    def determine_path_params(request_path: str) -> tuple:
        """ Метод возвращает компоненты пути в кортеже"""
        path = urlparse(request_path).path
        path_params = tuple(path.split('/')[2:])
        return path_params
