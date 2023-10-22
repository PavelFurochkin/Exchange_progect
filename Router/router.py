from urllib.parse import urlparse

from Controller import *


routes = {
    'currencies': CurrenciesController,
    'currency': CurrencyController,
    'exchangeRates': ExchangeRates,
    'exchangeRate': ExchangeRate,
    'exchange': ExchangeCurrency
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
        path = urlparse(request_path).path.split('/')[2]
        path_params = tuple((path[:3], path[3:]))
        return path_params
