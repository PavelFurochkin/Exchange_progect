from http.client import HTTPException

from Controller.base_controller import BaseController
from urllib.parse import urlparse
from Service.currencies_service import CurrenciesService
from DAO import CurrenciesDAO


class ExchangeCurrency(BaseController):
    """Контроллер для обраработки эндпойнтов конвертации валют

    Attributes
    ----------
    handler
        Контроллер для обработки пути
    dao
        Экземпляр класса для создания и проверки данных из базы данных

    Methods
    -------
    do_GET
        Обрабатывает запрос на получение обменного курса и результата обмена
    """
    def __init__(self, handle):
        super().__init__(handle)
        self.handle = handle
        self.dao = CurrenciesDAO()

    def do_GET(self):
        try:
            path_query = urlparse(self.handle.path.split('/')[1]).query
            path_split = path_query.split('&')
            result_dict = {}

            for item in path_split:
                key, value = item.split('=')
                result_dict[key] = value

            response = CurrenciesService().converting_currency(result_dict)
            self.send(200, response)
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
            raise HTTPException
        except Exception as error:
            self.error_handler(error)
        finally:
            self.dao.close()
