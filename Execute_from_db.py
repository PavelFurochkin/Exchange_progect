import sqlite3


class ExecuteBdCurrency:
    def __init__(self, data_base, table):
        self.data_base = data_base
        self.table = table

    def execute(self):
        conn = sqlite3.connect(self.data_base)
        cur = conn.cursor()

        # Выполняем запрос для получения всех записей из таблицы Currencies
        cur.execute(f'SELECT * FROM {self.table}')
        rows = cur.fetchall()

        conn.close()
        return rows


class Currency:
    def __init__(self, id_table, code, full_name, sign):
        self.id = id_table
        self.code = code
        self.full_name = full_name
        self.sign = sign

    def currency_representation(self):
        item = {
            'ID': self.id,
            'Code': self.code,
            'FullName': self.full_name,
            'Sign': self.sign
        }
        return item
