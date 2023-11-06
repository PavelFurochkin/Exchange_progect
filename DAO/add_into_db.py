from DAO.DAO import CurrenciesDAO
from http.client import HTTPException
from DAO import GetFromDB
from my_exception import MyError


class AddIntoDB:
    """Реализует методы для добавления сущностей в базу данных

    Attributes
    ----------
    dao
        Экземпляр класса для создания и проверки данных из базы данных
    get_from_db
        Экземпляр класса для получения данных из базы данных

    Methods
    -------
    add_currency( code, fullname, sign)
        Добавляет конкретную валюту в базу
    add_exchange_course( base_currency_id, target_currency_id, rate)
        Добавляетт новый обменный курс в базу
    """
    def __init__(self):
        self.dao = CurrenciesDAO()
        self.get_from_db = GetFromDB()

    def add_currency(self, code: str, fullname: str, sign: str) -> None:
        cursor = self.dao.conn.cursor()
        try:
            cursor.execute(
                """INSERT INTO Currencies(Code, FullName, Sign) VALUES(?,?,?)""", (code, fullname, sign)
            )
            self.dao.conn.commit()
        except HTTPException:
            raise HTTPException

    def add_exchange_course(self, base_currency_id: int, target_currency_id: int, rate: float) -> None:
        # Проверяем наличия обменного курса в базе
        if self.get_from_db.get_exchange_rate_by_id(base_currency_id, target_currency_id):
            raise MyError()  # Если курс уже есть в базе вызывает ошибку
        # Условие проверяет наличие валют для создания новой валютной пары
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
