from DAO import GetFromDB, CurrenciesDAO
from DTO import ExchangeCurrency, CurrencyDTO
from Mapper.mapper import Mapper

class CurrenciesService:
    def __init__(self):
        self.get_db = GetFromDB()
        self.dao = CurrenciesDAO()

    def converting_currency(self, request: dict):
        id_from: int = self.get_db.get_id_by_code(request.get('from'))
        id_to: int = self.get_db.get_id_by_code(request.get('to'))

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
            result = Mapper().exchange_rate_via_usd(
                id_from,
                id_to,
                usd_exchange[0],
                float(request.get('amount')),
                usd_exchange[1]
            )
            return result

    def __currency_exchange(self, base_currency, target_currency, amount, right: bool = True):
        exchange_pair = self.get_db.get_exchange_rate_by_id(
            base_currency, target_currency)
        if right:
            self.converting_result = float(exchange_pair.get('rate')) * float(amount)
        else:
            self.converting_result = 1 / float(exchange_pair.get('rate')) * float(amount)
        formatted_data = ExchangeCurrency(
            exchange_pair.get('baseCurrency'),
            exchange_pair.get('targetCurrency'),
            float(exchange_pair.get('rate')),
            float(amount),
            self.converting_result
        ).to_dict()
        return formatted_data

    def __exchange_via_USD(self, base_currency, target_currency, amount):
        change_base = self.get_db.get_exchange_rate_by_id(
            self.get_db.get_id_by_code('USD'),
            self.get_db.get_id_by_code(base_currency)
        )
        change_target = self.get_db.get_exchange_rate_by_id(
            self.get_db.get_id_by_code('USD'),
            self.get_db.get_id_by_code(target_currency)
        )
        exchange_rate: float = round(float(change_base.get('rate'))/float(change_target.get('rate')), 3)
        converted_amount: float = round(exchange_rate * amount, 3)
        return exchange_rate, converted_amount

