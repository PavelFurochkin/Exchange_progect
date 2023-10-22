from DAO.DAO import CurrenciesDAO

class GetFromDB:
    def __init__(self):
        self.dao = CurrenciesDAO()

    def get_all_currencies(self):
        cursor = self.dao.conn.cursor()
        __raw_list = cursor.execute(f'SELECT * FROM Currencies').fetchall()
        __prepare_list = []
        for each in __raw_list:
            __prepare_list.append(self.dao.formatting_for_currencies(each))
        return __prepare_list

    def get_all_exchange_rate(self):
        cursor = self.dao.conn.cursor()
        __raw_list = cursor.execute(f'SELECT * FROM ExchangeRates').fetchall()
        __prepare_list = []
        for each in __raw_list:
            __prepare_list.append(self.dao.formatting_for_exchange_rates(each))
        return __prepare_list

    def get_exchange_rate_by_code(self, base_currency: str, target_currency: str):
        cursor = self.dao.conn.cursor()
        __raw_list = cursor.execute(f'SELECT * FROM ExchangeRates').fetchall()
        try:
            for each in __raw_list:
                if each[1] == base_currency and each[2] == target_currency:
                    response = self.dao.formatting_for_exchange_rates(each)
                    return response
        except Exception as error:
            raise ValueError

    def get_currency_by_code(self, currency_code):
        cursor = self.dao.conn.cursor()
        raw_el = cursor.execute(f'SELECT * FROM Currencies WHERE Code = ?', (currency_code,)).fetchone()
        __response_code = self.dao.formatting_for_currencies(raw_el)
        if __response_code is None:
            raise ValueError
        return __response_code
