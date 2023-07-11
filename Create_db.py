import sqlite3

conn = sqlite3.connect('Exchange_base.db')
cur = conn.cursor()


cur.execute("""CREATE TABLE IF NOT EXISTS Currencies (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Code VARCHAR,
    FullName VARCHAR,
    Sign VARCHAR
);
""")

conn.commit()

cur.execute("""CREATE TABLE IF NOT EXISTS ExchangeRates (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    BaseCurrencyId INTEGER,
    TargetCurrencyId INTEGER,
    Rate Decimal(6),
    FOREIGN KEY (BaseCurrencyId) REFERENCES Currencies (ID)
    FOREIGN KEY (TargetCurrencyId) REFERENCES Currencies (ID)
);
""")
conn.commit()

cur.execute("""INSERT INTO Currencies VALUES('1', 'AUD', 'Australian dollar', 'A$' )
""")

cur.execute("""INSERT INTO Currencies VALUES('2', 'CNY', 'Yuan Renminbi', '¥' )
""")

cur.execute("""INSERT INTO Currencies VALUES('3', 'EUR', 'Euro', '€' )
""")

cur.execute("""INSERT INTO Currencies VALUES('4', 'USD', 'US Dollar', '$' )
""")

cur.execute("""INSERT INTO Currencies VALUES('5', 'RUB', 'Russian Ruble', '₽' )
""")

# conn.execute("DROP TABLE Currencies")

conn.commit()

conn.close()
