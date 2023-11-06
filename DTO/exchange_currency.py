from DTO.currency_dto import CurrencyDTO


class ExchangeCurrency:

    def __init__(self, base_currency: tuple, target_currency: tuple,
                 rate: float, amount: float, converted_amount: float):
        self.baseCurrency = CurrencyDTO(base_currency).to_dict()
        self.targetCurrency = CurrencyDTO(target_currency).to_dict()
        self.rate = rate
        self.amount = amount
        self.converted_amount = converted_amount

    def to_dict(self):
        return self.__dict__
