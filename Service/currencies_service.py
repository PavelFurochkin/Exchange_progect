from DAO import GetFromDB, CurrenciesDAO
from decimal import *
from Mapper.mapper import Mapper



class CurrenciesService:
    """Реализует логику получения обменного курса из базы данных

    Attributes
    ----------
    dao
        Экземпляр класса для создания и проверки данных из базы данных
    get_db
        Экземпляр класса для получения данных из базы данных

    Methods
    -------
    converting_currency(request)
        Реализует конвертацию из одной валюты в другую
    __currency_exchange(base_currency, target_currency, amount, right)
        Формирует представление обменного курса по имеющемуся в базе курсу
    __exchange_via_USD(self, base_currency, target_currency, amount)
        Формирует представление обменного курса через курс USD
    """
    getcontext().prec = 4

    def __init__(self):
        self.get_db = GetFromDB()
        self.dao = CurrenciesDAO()

    def converting_currency(self, request: dict):
        # Для удобства достаем из базы ID запрашиваемых валют
        id_from: int = self.get_db.get_id_by_code(request.get('from'))
        id_to: int = self.get_db.get_id_by_code(request.get('to'))
        # Получаем обменные курсы из бд, если их нет - конвертируем через USD
        if self.get_db.get_exchange_rate_by_id(id_from, id_to):
            return self.__currency_exchange(
                id_from, id_to, request.get('amount')
            )
        elif self.get_db.get_exchange_rate_by_id(id_to, id_from):
            return self.__currency_exchange(
                id_to, id_from, request.get('amount'), False
            )
        else:
            usd_exchange = self.__exchange_via_USD(
                request.get('from'), request.get('to'), float(request.get('amount')))
            result = Mapper().presenting_exchange_rate(
                id_from,
                id_to,
                round(float(usd_exchange[0]), 4),
                float(request.get('amount')),
                round(float(usd_exchange[1]), 4)
            )
            return result

    def __currency_exchange(self, base_currency, target_currency, amount, right: bool = True) -> dict:
        # Получаем обменный курс
        exchange_pair = self.get_db.get_exchange_rate_by_id(
            base_currency, target_currency)

        if right:
            self.converting_result = Decimal(exchange_pair.get('rate')) * Decimal(amount)
            formatted_data = Mapper().presenting_exchange_rate(
                exchange_pair['baseCurrency']['id'],
                exchange_pair['targetCurrency']['id'],
                float(exchange_pair.get('rate')),
                float(amount),
                round(float(self.converting_result), 2)
            )
        else:
            self.converting_result = 1 / Decimal(exchange_pair.get('rate')) * Decimal(amount)
            rate = 1 / Decimal(exchange_pair.get('rate'))
            formatted_data = Mapper().presenting_exchange_rate(
                exchange_pair['targetCurrency']['id'],
                exchange_pair['baseCurrency']['id'],
                float(rate),
                float(amount),
                round(float(self.converting_result), 2)
            )
        return formatted_data

    def __exchange_via_USD(self, base_currency, target_currency, amount):
        # получаем обменный курс базовой валюты через USD
        change_base = self.get_db.get_exchange_rate_by_id(
            self.get_db.get_id_by_code('USD'),
            self.get_db.get_id_by_code(base_currency)
        )
        # получаем обменный курс целевой валюты через USD
        change_target = self.get_db.get_exchange_rate_by_id(
            self.get_db.get_id_by_code('USD'),
            self.get_db.get_id_by_code(target_currency)
        )
        # Вычисляем обменный курс
        exchange_rate: Decimal = Decimal(change_base.get('rate'))/Decimal(change_target.get('rate'))
        converted_amount = exchange_rate * Decimal(amount)
        return exchange_rate, converted_amount

