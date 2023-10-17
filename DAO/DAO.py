import sqlite3
from http.client import HTTPException


class CurrenciesDAO:
    db_name = 'exchange_base.db'

    def __init__(self):
        self.conn = sqlite3.connect(self.db_name)
        self.__create_table()

    def __create_table(self):
        cursor = self.conn.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS Currencies (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Code VARCHAR,
            FullName VARCHAR,
            Sign VARCHAR
            );
            """)
        self.conn.commit()

        cursor.execute("""CREATE TABLE IF NOT EXISTS ExchangeRates (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            BaseCurrencyId INTEGER,
            TargetCurrencyId INTEGER,
            Rate Decimal(6,4),
            FOREIGN KEY (BaseCurrencyId) REFERENCES Currencies (ID)
            FOREIGN KEY (TargetCurrencyId) REFERENCES Currencies (ID)
        );
        """)
        self.conn.commit()

        cursor.execute('SELECT COUNT(*) FROM Currencies')
        count_currencies = cursor.fetchone()[0]

        if count_currencies == 0:
            cursor.execute("""INSERT INTO Currencies VALUES('1', 'AUD', 'Australian dollar', 'A$' )""")
            cursor.execute("""INSERT INTO Currencies VALUES('2', 'CNY', 'Yuan Renminbi', '¥' )""")
            cursor.execute("""INSERT INTO Currencies VALUES('3', 'EUR', 'Euro', '€' )""")
            cursor.execute("""INSERT INTO Currencies VALUES('4', 'USD', 'US Dollar', '$' )""")
            cursor.execute("""INSERT INTO Currencies VALUES('5', 'RUB', 'Russian Ruble', '₽' )""")
            self.conn.commit()

        cursor.execute('SELECT COUNT(*) FROM ExchangeRates')
        count_exchange = cursor.fetchone()[0]

        if count_exchange == 0:
            cursor.execute("""INSERT INTO ExchangeRates VALUES('1', '5', '4', '0.01')""")
            cursor.execute("""INSERT INTO ExchangeRates VALUES('2', '4', '3', '0.95')""")
            cursor.execute("""INSERT INTO ExchangeRates VALUES('3', '2', '4', '0.006')""")
            self.conn.commit()

    def add_currency(self, code: str, fullname: str, sign: str):
        try:
            self.conn.cursor().execute(
                """INSERT INTO Currencies(Code, FullName, Sign) VALUES(?,?,?)""", (code, fullname, sign)
            )
            self.conn.commit()
        except HTTPException:
            raise HTTPException

    def get_all_currencies(self):
        cursor = self.conn.cursor()
        __raw_list = cursor.execute(f'SELECT * FROM Currencies').fetchall()
        __prepare_list = []
        for each in __raw_list:
            __prepare_list.append(self.formatted_response(each))
        return __prepare_list

    def get_all_exchange_rate(self):
        cursor = self.conn.cursor()
        __raw_list = cursor.execute(f'SELECT * FROM ExchangeRates').fetchall()
        __prepare_list = []
        for each in __raw_list:
            __prepare_list.append(self.exchange_formatted_response(each))
        return __prepare_list

    def get_exchange_rate_by_code(self, base_currency: str, target_currency: str):
        cursor = self.conn.cursor()
        __raw_list = cursor.execute(f'SELECT * FROM ExchangeRates').fetchall()
        try:
            for each in __raw_list:
                if each[1] == base_currency and each[2] == target_currency:
                    responce = self.exchange_formatted_response(each)
                    return responce
        except Exception as error:
            pass

    def get_currency_by_code(self, currency_code):
        cursor = self.conn.cursor()
        raw_el = cursor.execute(f'SELECT * FROM Currencies WHERE Code = ?', (currency_code,)).fetchone()
        __response_code = self.formatted_response(raw_el)
        if __response_code is None:
            raise ValueError
        return __response_code

    def check_code(self, code: str):
        check_code = self.conn.cursor().execute(
            """SELECT Code FROM Currencies WHERE Code = ?""", (code,)
        ).fetchone()
        if check_code and check_code[0] == code:
            return True
        return False

    def formatted_response(self, data):
        formatted_data = {
            "id": data[0],
            "name": data[1],
            "code": data[2],
            "sign": data[3]
        }
        return formatted_data

    def exchange_formatted_response(self, data):
        cursor = self.conn.cursor()
        __base_currency = cursor.execute(
            f'SELECT * FROM Currencies WHERE ID = ?', (data[1],)
        ).fetchone()
        __target_currency = cursor.execute(
            f'SELECT * FROM Currencies WHERE ID = ?', (data[2],)
        ).fetchone()
        formatted_data = {
            "id": data[0],
            "baseCurrency": self.formatted_response(__base_currency),
            "targetCurrency": self.formatted_response(__target_currency),
            "rate": data[3]
        }
        return formatted_data


    def close(self):
        self.conn.close()
