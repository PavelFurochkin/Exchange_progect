from urllib.parse import parse_qs
from http.client import HTTPException

from Controller.base_controller import BaseController
from DAO import CurrenciesDAO, GetFromDB


class ExchangeRate(BaseController):
    """Используется для получения всех обменных курсов, а также изменения существующего курса

    Attributes
    ----------
    handler
        Контроллер для обработки пути
    dao
        Экземпляр класса для создания и проверки данных из базы данных
    from_dao
        Экземпляр класса для получения данных из базы данных

    Methods
    -------
    do_GET
        Обрабатывает запрос на вывод конкретного обменного курса
    do_PATCH
        Обрабатывает запрос на изменение волюты в базе
    """
    def __init__(self, handler):
        super().__init__(handler),
        self.from_dao = GetFromDB()
        self.dao = CurrenciesDAO()

    def do_GET(self):
        try:
            __path = self.handler.path.split('/')[2]  # Получаем валютную пару
            __path_params = tuple((__path[:3], __path[3:]))  # Разбиваем валютную пару на отдельные валюты
            __base_currency: int = self.from_dao.get_currency_by_code(__path_params[0]).get('id')
            __target_currency: int = self.from_dao.get_currency_by_code(__path_params[1]).get('id')
            __response = self.from_dao.get_exchange_rate_by_id(__base_currency, __target_currency)
            self.send(200, __response)
            self.dao.close()
        except Exception as error:
            self.error_handler(error)

    def do_POST(self):
        try:
            raise HTTPException
        except Exception as error:
            self.error_handler(error)
        finally:
            self.dao.close()

    def do_PATCH(self):
        try:
            __rate = 0
            __content_type = self.handler.headers.get('Content-Type', '')  # Получаем тип кодировки данных
            if __content_type.strip() == 'application/x-www-form-urlencoded':
                # Получаем количество байт данных, которые следует прочитать из тела запроса
                content_length = int(self.handler.headers['content-length'])
                # Декодируем байты через utf-8 в текстовое представление
                post_data = self.handler.rfile.read(content_length).decode('utf-8')
                # разбирает строку и создает словарь, ключи - имена полей формы, а значения — списки значений полей
                form_data = parse_qs(post_data)
                __rate = float(form_data.get('rate', '')[0])

            __path = self.handler.path.split('/')[2]  # Получаем валютную пару
            __path_params = tuple((__path[:3], __path[3:]))  # Разбиваем валютную пару на отдельные валюты
            __base_currency = self.from_dao.get_currency_by_code(__path_params[0]).get('id')
            __target_currency = self.from_dao.get_currency_by_code(__path_params[1]).get('id')
            # Получаем полное представление обменного курса
            __pair_for_patch = self.from_dao.get_exchange_rate_by_id(__base_currency, __target_currency)
            #  Изменяем курс в валютной паре на новый
            __response = self.dao.update_data(__pair_for_patch.get('id'), __rate)
            __fresh_pair = self.from_dao.get_exchange_rate_by_id(__base_currency, __target_currency)
            self.send(200, __fresh_pair)
            self.dao.close()
        except Exception as error:
            self.error_handler(error)
