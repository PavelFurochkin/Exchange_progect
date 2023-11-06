from http.client import HTTPException

from Controller.base_controller import BaseController
from DAO import CurrenciesDAO, GetFromDB


class CurrencyController(BaseController):
    """Используется для получения всех валют, а также добавления новой валюты в базу

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
        Обрабатывает запрос на вывод одной валюты из базы данных
    do_POST
        Вызывает ошибку при обращении к методу по этому эндпойнту
    """
    def __init__(self, handler):
        self.dao = CurrenciesDAO()
        self.from_dao = GetFromDB()
        super().__init__(handler)

    def do_GET(self):
        try:
            code = self.handler.path.split('/')[-1]  # Получаем код валюты из пути
            if code == '':
                raise HTTPException  # Вызаваем ошибку при получении пустой строки
            # Получаем представление валюты по коду
            currency = self.from_dao.get_currency_by_code(code)
            self.send(200, currency)
        except Exception as error:
            self.error_handler(error)
        finally:
            self.dao.close()

    def do_POST(self):
        try:
            raise HTTPException
        except Exception as error:
            self.error_handler(error)
        finally:
            self.dao.close()
