import sqlite3
from http.client import HTTPException


class CurrenciesDAO:
    db_name = 'Exchange_base.db'

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
            Rate Decimal(6),
            FOREIGN KEY (BaseCurrencyId) REFERENCES Currencies (ID)
            FOREIGN KEY (TargetCurrencyId) REFERENCES Currencies (ID)
        );
        """)
        self.conn.commit()

        cursor.execute('SELECT COUNT(*) FROM Currencies')
        count = cursor.fetchone()[0]

        if count == 0:
            cursor.execute("""INSERT INTO Currencies VALUES('1', 'AUD', 'Australian dollar', 'A$' )""")
            cursor.execute("""INSERT INTO Currencies VALUES('2', 'CNY', 'Yuan Renminbi', '¥' )""")
            cursor.execute("""INSERT INTO Currencies VALUES('3', 'EUR', 'Euro', '€' )""")
            cursor.execute("""INSERT INTO Currencies VALUES('4', 'USD', 'US Dollar', '$' )""")
            cursor.execute("""INSERT INTO Currencies VALUES('5', 'RUB', 'Russian Ruble', '₽' )""")
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
        raw_list = cursor.execute(f'SELECT * FROM Currencies').fetchall()
        formatted_list = self.formatted_response(raw_list)
        return formatted_list

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
        final_list = []
        for each in data:
            formatted_data = {
                "id": each[0],
                "name": each[1],
                "code": each[2],
                "sign": each[3]
            }
            final_list.append(formatted_data)
        return final_list

    def close(self):
        self.conn.close()
