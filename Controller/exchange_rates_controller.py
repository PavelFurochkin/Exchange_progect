from http.client import HTTPException

from Controller.base_controller import BaseController
from DAO import CurrenciesDAO, GetFromDB, AddIntoDB
from urllib.parse import parse_qs


class ExchangeRates(BaseController):
    """Используется для добавления нового обменного курса в базу

    Attributes
    ----------
    handler
        Контроллер для обработки пути
    dao
        Экземпляр класса для создания и проверки данных из базы данных
    from_dao
        Экземпляр класса для получения данных из базы данных
    add_in_dao
        Экземпляр класса для добавления данных в базу

    Methods
    -------
    do_GET
        Обрабатывает запрос на вывод всех обменных курсов из базы данных
    do_POST
        Обрабатывает запрос на добавление нового обменного в базу данных
    """
    def __init__(self, handler):
        super().__init__(handler),
        self.dao = CurrenciesDAO()
        self.from_dao = GetFromDB()
        self.add_in_dao = AddIntoDB()

    def do_GET(self):
        try:
            currencies_exchange = self.from_dao.get_all_exchange_rate()
            self.send(200, currencies_exchange)
            self.dao.close()
        except Exception as error:
            self.error_handler(error)

    def do_POST(self):
        try:
            content_type = self.handler.headers.get('Content-Type', '')  # Получаем тип кодировки данных
            if content_type.strip() == 'application/x-www-form-urlencoded':
                # Получаем количество байт данных, которые следует прочитать из тела запроса
                content_length: int = int(self.handler.headers['content-length'])
                # Декодируем байты через utf-8 в текстовое представление
                post_data = self.handler.rfile.read(content_length).decode('utf-8')
                # Разбирает строку и создает словарь, ключи - имена полей формы, а значения — списки значений полей
                form_data = parse_qs(post_data)
                base_currency_code: str = form_data.get('baseCurrencyCode', '')[0]
                target_currency_code: str = form_data.get('targetCurrencyCode', '')[0]
                rate: float = float(form_data.get('rate', '')[0])
                #  Получаем id по коду валюты
                base_currency_id = self.from_dao.get_currency_by_code(base_currency_code).get('id')
                target_currency_id = self.from_dao.get_currency_by_code(target_currency_code).get('id')
                #  Добавляем новую пару в базу данных
                self.add_in_dao.add_exchange_course(base_currency_id, target_currency_id, rate)
                added_exchange_rate = self.from_dao.get_exchange_rate_by_id(
                    base_currency_id, target_currency_id)
                self.send(200, added_exchange_rate)
            else:
                raise HTTPException
        except Exception as error:
            self.error_handler(error)
        finally:
            self.dao.close()

