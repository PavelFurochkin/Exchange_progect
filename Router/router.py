from urllib.parse import urlparse

from Controller import *

# Через эндпойнты определяем целевой контроллер
routes = {
    'currencies': CurrenciesController,
    'currency': CurrencyController,
    'exchangeRates': ExchangeRates,
    'exchangeRate': ExchangeRate,
    'exchange': ExchangeCurrency
}

class PathRouter:
    """Реализует логику получения обменного курса из базы данных

        Methods
        -------
        determine_controller_class_by_path(request_path)
            Разбирает URL-адрес, вычленяя последний элемент пути
    """
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
