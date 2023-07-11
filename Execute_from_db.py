import sqlite3


class ExecuteBd:

    conn = sqlite3.connect('Exchange_base.db')
    cur = conn.cursor()

    # Выполняем запрос для получения всех записей из таблицы Currencies
    cur.execute("SELECT * FROM Currencies")
    rows = cur.fetchall()

    conn.close()
