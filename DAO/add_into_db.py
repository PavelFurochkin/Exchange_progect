from DAO.DAO import CurrenciesDAO
from http.client import HTTPException
from DAO import GetFromDB
from my_exception import MyError


class AddIntoDB:
    def __init__(self):
        self.dao = CurrenciesDAO()
        self.get_from_db = GetFromDB()

    def add_currency(self, code: str, fullname: str, sign: str):
        cursor = self.dao.conn.cursor()
        try:
            cursor.execute(
                """INSERT INTO Currencies(Code, FullName, Sign) VALUES(?,?,?)""", (code, fullname, sign)
            )
            self.dao.conn.commit()
        except HTTPException:
            raise HTTPException

    def add_exchange_course(self, base_currency_id: int, target_currency_id: int, rate: float):
        if self.get_from_db.get_exchange_rate_by_id(base_currency_id, target_currency_id):
            raise MyError()
        elif self.dao.check_id(base_currency_id) and self.dao.check_id(target_currency_id):
            cursor = self.dao.conn.cursor()
            cursor.execute(f'INSERT INTO ExchangeRates('
                           f'BaseCurrencyID, TargetCurrencyID, Rate)'
                           f'VALUES( ?, ?, ?)',
                           (base_currency_id, target_currency_id, rate)
                           )
            self.dao.conn.commit()
        else:
            raise HTTPException
