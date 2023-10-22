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

    def check_code(self, code: str):
        check_code = self.conn.cursor().execute(
            """SELECT Code FROM Currencies WHERE Code = ?""", (code,)
        ).fetchone()
        if check_code and check_code[0] == code:
            return True
        return False

    def formatting_for_currencies(self, data):
        formatted_data = {
            "id": data[0],
            "name": data[1],
            "code": data[2],
            "sign": data[3]
        }
        return formatted_data

    def formatting_for_exchange_rates(self, data):
        cursor = self.conn.cursor()
        __base_currency = cursor.execute(
            """SELECT * FROM Currencies WHERE ID = ?""", (data[1],)
        ).fetchone()
        __target_currency = cursor.execute(
            """SELECT * FROM Currencies WHERE ID = ?""", (data[2],)
        ).fetchone()
        formatted_data = {
            "id": data[0],
            "baseCurrency": self.formatting_for_currencies(__base_currency),
            "targetCurrency": self.formatting_for_currencies(__target_currency),
            "rate": data[3]
        }
        return formatted_data

    def update_data(self, pair_id: int, rate: float):
        cursor = self.conn.cursor()
        cursor.execute(
            """
            UPDATE ExchangeRates
            SET Rate = ?
            WHERE ID = ?
            """, (rate, pair_id)
        ).fetchone()
        self.conn.commit()
        response = cursor.execute(
            """SELECT * FROM ExchangeRates WHERE ID = ?""", (pair_id,)
        ).fetchone()
        return response

    def close(self):
        self.conn.close()
