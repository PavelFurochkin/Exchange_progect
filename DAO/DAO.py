import sqlite3


class CurrenciesDAO:
    """Реализует методы для создания, проверки и обновления базы данных

    Attributes
    ----------
    conn
        Подключает к созданной базе данный
    __create_table()
        Создает базу данных, если таковой нет

    Methods
    -------
    __create_table()
        Создает новую базу и наполняет её содержимым, если базы данных нет
    check_code(code)
        Проверяет наличие валюты в базе по коду
    check_id(id)
        Проверяет наличие валюты в базе по id
    update_data(pair_id, rate)
        Меняет обменный курс в существующей базе
    close()
        Завершает работу с базой данных
    """
    db_name = 'Exchange_base.db'

    def __init__(self):
        self.conn = sqlite3.connect(self.db_name)
        self.__create_table()

    def __create_table(self):
        cursor = self.conn.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS Currencies (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Code VARCHAR UNIQUE,
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

    def check_id(self, id: int):
        check_code = self.conn.cursor().execute(
            """SELECT ID FROM Currencies WHERE ID = ?""", (id,)
        ).fetchone()
        if check_code and check_code[0] == id:
            return True
        return False

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
