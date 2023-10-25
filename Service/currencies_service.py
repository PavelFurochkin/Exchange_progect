from DAO import GetFromDB, CurrenciesDAO

class CurrenciesService:
    def __init__(self):
        self.get_db = GetFromDB()
        self.dao = CurrenciesDAO()

    def converting_currency(self, request: dict):

        if self.get_db.get_exchange_rate_by_code(request.get('from'), request.get('to')):
            return self.__currency_exchange(
                request.get('from'), request.get('to'), request.get('amount')
            )
        elif self.get_db.get_exchange_rate_by_code(request.get('to'), request.get('from')):
            return self.__currency_exchange(
                request.get('to'), request.get('from'), request.get('amount'), False
            )
        else:
            amount_exchange = self.__exchange_via_USD(
                request.get('from'), request.get('to'), request.get('amount'))
            result = self.dao.formatting_for_exchange_rates((request.get('from'), request.get('to')))
            result.update(amount=amount_exchange)
            return result

    def __currency_exchange(self, base_currency, target_currency, amount, right: bool = True):
        exchange_pair = self.get_db.get_exchange_rate_by_code(
            base_currency, target_currency)
        converting_result = 0
        if right:
            self.converting_result = float(exchange_pair.get('rate')) * float(amount)
        else:
            self.converting_result = 1 / float(exchange_pair.get('rate')) * float(amount)
        formatted_data = {
            "baseCurrency": self.dao.formatting_for_currencies(base_currency),
            "targetCurrency": self.dao.formatting_for_currencies(target_currency),
            "rate": float(exchange_pair.get('rate')),
            "amount": float(amount),
            "convertedAmount": converting_result
        }
        return formatted_data

    def __exchange_via_USD(self, base_currency, target_currency, amount):
        change_base = self.get_db.get_exchange_rate_by_code('USD', base_currency)
        change_target = self.get_db.get_exchange_rate_by_code('USD', target_currency)
        exchange: float = (float(change_base.get('rate')) *
                           float(amount))/(float(change_target.get('rate')) *
                                           float(amount))
        return exchange

