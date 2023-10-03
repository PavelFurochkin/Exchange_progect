import sqlite3


class CurrenciesDAO:
    db_name = 'Exchange_base1.db'

    def __init__(self):
        self.conn = sqlite3.connect(self.db_name)
        # self.__create_table()

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

    def get_all_currencies(self):
        cursor = self.conn.cursor()
        cursor.execute(f'SELECT * FROM Currencies')
        return cursor.fetchall()

    def get_currency_by_code(self, currency_code):
        cursor = self.conn.cursor()
        cursor.execute(f'SELECT * FROM Currencies WHERE Code = ?', (currency_code,))
        return cursor.fetchone()

    def close(self):
        self.conn.close()
