from DTO.currency_dto import CurrencyDTO


class ExchangeRatesDTO:

    def __init__(self, id_rate: int, base_currency: tuple, target_currency: tuple, rate: float):
        self.id = id_rate
        self.baseCurrency = CurrencyDTO(base_currency).to_dict()
        self.targetCurrency = CurrencyDTO(target_currency).to_dict()
        self.rate = rate

    def to_dict(self):
        return self.__dict__
