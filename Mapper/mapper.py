import sqlite3

from DAO.DAO import CurrenciesDAO
from DTO import ExchangeRatesDTO, ExchangeCurrency


class Mapper:
    """Реализует работу с базой данных и формирование представления

    Attributes
    ----------
    dao
        Экземпляр класса для создания и проверки данных из базы данных
    conn
        Реализует подключение к базе данных

    Methods
    -------
    exchange_rate_model_to_dao(data)
        Получает данные по валютам из базы и формирует представление обменного курса
    exchange_rate_via_usd(id_base, id_target, rate, amount, converted_amount)
        Получает данные по валютам из базы и формирует представление обменного курса
        через валюту USD
    """
    db_name = 'Exchange_base.db'

    def __init__(self):
        self.dao = CurrenciesDAO()
        self.conn = sqlite3.connect(self.db_name)

    def exchange_rate_model_to_dao(self, data) -> dict:
        cursor = self.conn.cursor()
        __base_currency = cursor.execute(
            """SELECT * FROM Currencies WHERE ID = ?""", (data[1],)
        ).fetchone()
        __target_currency = cursor.execute(
            """SELECT * FROM Currencies WHERE ID = ?""", (data[2],)
        ).fetchone()
        # Формирует представление обменного курса через DTO
        formatted_data = ExchangeRatesDTO(data[0], __base_currency, __target_currency, data[3]).to_dict()
        return formatted_data

    def exchange_rate_via_usd(self, id_base: int, id_target: int,
                              rate: float, amount: float, converted_amount: float) -> dict:
        cursor = self.conn.cursor()
        __base_currency = cursor.execute(
            """SELECT * FROM Currencies WHERE ID = ?""", (id_base,)
        ).fetchone()
        __target_currency = cursor.execute(
            """SELECT * FROM Currencies WHERE ID = ?""", (id_target,)
        ).fetchone()
        # Формирует представление обменного курса через DTO
        formatted_data = ExchangeCurrency(__base_currency, __target_currency, rate,
                                          amount, converted_amount).to_dict()
        return formatted_data
