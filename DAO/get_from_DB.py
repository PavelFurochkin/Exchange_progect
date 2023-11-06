from DAO.DAO import CurrenciesDAO
from DTO.currency_dto import CurrencyDTO
from Mapper.mapper import Mapper


class GetFromDB:
    """Реализует методы для получения сущностей из базы данных

    Attributes
    ----------
    dao
        Экземпляр класса для создания и проверки данных из базы данных

    Methods
    -------
    get_all_currencies()
        Возвращает список со всеми валютами
    get_all_exchange_rate()
        Возвращает список со всеми обменными курсами
    get_exchange_rate_by_id(base_currency, target_currency)
        Возвращает валютную пару по id
    get_currency_by_code(currency_code)
        Возвращает валюту по коду валюты
    get_id_by_code(code)
        Возвращает id валюты по её коду
    """
    def __init__(self):
        self.dao = CurrenciesDAO()

    def get_all_currencies(self) -> list:
        cursor = self.dao.conn.cursor()
        __raw_list = cursor.execute(f'SELECT * FROM Currencies').fetchall()
        __prepare_list = []
        for each in __raw_list:
            __prepare_list.append(CurrencyDTO(each).to_dict())
        return __prepare_list

    def get_all_exchange_rate(self) -> list:
        cursor = self.dao.conn.cursor()
        __raw_list = cursor.execute(f'SELECT * FROM ExchangeRates').fetchall()
        __prepare_list = []
        for each in __raw_list:
            # Добавляем полное представление обменного курса в список
            __prepare_list.append(Mapper().exchange_rate_model_to_dao(each))
        return __prepare_list

    def get_exchange_rate_by_id(self, base_currency: int, target_currency: int) -> dict:
        cursor = self.dao.conn.cursor()
        __raw_list = cursor.execute(f'SELECT * FROM ExchangeRates').fetchall()
        try:
            for each in __raw_list:
                # Провеляем наличие обменного курса в базе
                if each[1] == base_currency and each[2] == target_currency:
                    # Возвращаем полное представление валютной пары
                    response = Mapper().exchange_rate_model_to_dao(each)
                    return response
        except Exception:
            raise ValueError

    def get_currency_by_code(self, currency_code) -> dict:
        cursor = self.dao.conn.cursor()
        __raw_el = cursor.execute(f'SELECT * FROM Currencies WHERE Code = ?', (currency_code,)).fetchone()
        __response_code = CurrencyDTO(__raw_el).to_dict()
        if __response_code is None:
            raise ValueError
        return __response_code

    def get_id_by_code(self, code: str) -> int:
        cursor = self.dao.conn.cursor()
        __check_code = cursor.execute(
            """SELECT ID FROM Currencies WHERE Code = ?""", (code,)
        ).fetchone()
        return __check_code[0]
