from DAO.DAO import CurrenciesDAO
from http.client import HTTPException
from DAO import GetFromDB
from my_exception import MyError


class AddIntoDB:
    def __int__(self):
        self.dao = CurrenciesDAO()
        self.get_from_db = GetFromDB()

    def add_currency(self, code: str, fullname: str, sign: str):
        cursor = self.dao.conn.cursor()
        try:
            cursor.execute(
                """INSERT INTO Currencies(Code, FullName, Sign) VALUES(?,?,?)""", (code, fullname, sign)
            )
            cursor.commit()
        except HTTPException:
            raise HTTPException

    def add_exchange_course(self, base_currency_code: str, target_currency_code: str, rate: float):
        if self.get_from_db.get_exchange_rate_by_code(base_currency_code, target_currency_code):
            raise MyError()
        elif self.dao.check_code(base_currency_code) and self.dao.check_code(target_currency_code):
            cursor = self.dao.conn.cursor()
            cursor.execute(f'INSERT INTO ExchangeRates('
                           f'BaseCurrencyID, TargetCurrencyID, Rate)'
                           f'VALUES( ?, ?, ?)',
                           (base_currency_code, target_currency_code, rate)
                           )
            cursor.commit()
        else:
            raise HTTPException
