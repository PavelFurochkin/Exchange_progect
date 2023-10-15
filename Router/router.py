from urllib.parse import urlparse

from Controller.currencies_controller import CurrenciesController
from Controller.currency_controller import CurrencyController
from Controller.exchange_rates_controller import ExchangeRates
from Controller.exchange_rate_controller import ExchangeRate
from DAO.DAO import CurrenciesDAO

routes = {
    'currencies': CurrenciesController,
    'currency': CurrencyController,
    'exchangeRates': ExchangeRates,
    'exchangeRate': ExchangeRate
}

class PathRouter:
    @staticmethod
    def determine_controller_class_by_path(request_path: str):
        """ Медод позволяет получить путь"""
        path = urlparse(request_path).path
        split_path = path.split('/')
        if len(split_path) >= 2:
        #     param = split_path[2]
        #     check_param = CurrenciesDAO().check_code(param)
        #     if not check_param:
        #         raise ValueError
        # if len(split_path) >= 2:
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
