from urllib.parse import parse_qs
from http.client import HTTPException

from Controller.base_controller import BaseController
from DAO import CurrenciesDAO, GetFromDB, AddIntoDB


class CurrenciesController(BaseController):
    """Используется для получения всех валют, а также добавления новой валюты в базу

    Attributes
    ----------
    handler
        Контроллер для обработки пути
    dao
        Экземпляр класса для создания и проверки данных из базы данных
    from_dao
        Экземпляр класса для получения данных из базы данных
    add_in_db
        Экземпляр класса для добавления данных в базу

    Methods
    -------
    do_GET
        Обрабатывает запрос на вывод всех валют из базы данных
    do_POST
        Обрабатывает запрос на добавление новой волюты в базу данных
    """
    def __init__(self, handler):
        super().__init__(handler)
        self.dao = CurrenciesDAO()
        self.from_dao = GetFromDB()
        self.add_in_db = AddIntoDB()

    def do_GET(self):
        try:
            currencies = self.from_dao.get_all_currencies()
            self.send(200, currencies)
            self.dao.close()
        except Exception as error:
            self.error_handler(error)

    def do_POST(self):
        try:
            content_type: str = self.handler.headers.get('Content-Type', '')  # Получаем тип кодировки данных
            if content_type.strip() == 'application/x-www-form-urlencoded':
                # Получаем количество байт данных, которые следует прочитать из тела запроса
                content_length = int(self.handler.headers['content-length'])
                # Декодируем байты через utf-8 в текстовое представление
                post_data: str = self.handler.rfile.read(content_length).decode('utf-8')
                # разбирает строку и создает словарь, ключи - имена полей формы, а значения — списки значений полей
                form_data: dict = parse_qs(post_data)
                code: str = form_data.get('code','')[0]
                name: str = form_data.get('name','')[0]
                sing: str = form_data.get('sign','')[0]
                if self.dao.check_code(code):
                    error = 'Такая валюта уже есть в базе'
                    self.send(400, {'error': error})
                    return
                else:
                    self.add_in_db.add_currency(code, name, sing)
                    currency_code = self.from_dao.get_currency_by_code(code)
                    self.send(200, currency_code)
            else:
                raise HTTPException
        except Exception as error:
            self.error_handler(error)
        finally:
            self.dao.close()
