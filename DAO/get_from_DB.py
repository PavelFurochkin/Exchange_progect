from DAO.DAO import CurrenciesDAO
from DTO.currency_dto import CurrencyDTO
from Mapper.mapper import Mapper

class GetFromDB:
    def __init__(self):
        self.dao = CurrenciesDAO()

    def get_all_currencies(self):
        cursor = self.dao.conn.cursor()
        __raw_list = cursor.execute(f'SELECT * FROM Currencies').fetchall()
        __prepare_list = []
        for each in __raw_list:
            __prepare_list.append(CurrencyDTO(each).to_dict())
        return __prepare_list

    def get_all_exchange_rate(self):
        cursor = self.dao.conn.cursor()
        __raw_list = cursor.execute(f'SELECT * FROM ExchangeRates').fetchall()
        __prepare_list = []
        for each in __raw_list:
            __prepare_list.append(Mapper().exchange_rate_model_to_dao(each))
        return __prepare_list

    def get_exchange_rate_by_id(self, base_currency: int, target_currency: int) -> dict:
        cursor = self.dao.conn.cursor()
        __raw_list = cursor.execute(f'SELECT * FROM ExchangeRates').fetchall()
        try:
            for each in __raw_list:
                if each[1] == base_currency and each[2] == target_currency:
                    response = Mapper().exchange_rate_model_to_dao(each)
                    return response
        except Exception as error:
            raise ValueError

    def get_currency_by_code(self, currency_code) -> dict:
        cursor = self.dao.conn.cursor()
        raw_el = cursor.execute(f'SELECT * FROM Currencies WHERE Code = ?', (currency_code,)).fetchone()
        __response_code = CurrencyDTO(raw_el).to_dict()
        if __response_code is None:
            raise ValueError
        return __response_code

    def get_id_by_code(self, code: str):
        cursor = self.dao.conn.cursor()
        check_code = cursor.execute(
            """SELECT ID FROM Currencies WHERE Code = ?""", (code,)
        ).fetchone()
        return check_code[0]
