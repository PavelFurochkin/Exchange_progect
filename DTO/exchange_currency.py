from DTO.currency_dto import CurrencyDTO


class ExchangeCurrency:
    """Создает DTO для конкретной валюты

    Attributes
    ----------
    baseCurrency
        представление базовой валюты
    targetCurrency
        представление целевой валюты
    rate
        обменный курс пары
    amount
        количество к обмену
    converted_amount
        итоговая сумма обмена

    Methods
    -------
    to_dict()
        Возвращает представление обменного курса в словаре
    """

    def __init__(self, base_currency: tuple, target_currency: tuple,
                 rate: float, amount: float, converted_amount: float):
        self.baseCurrency = CurrencyDTO(base_currency).to_dict()
        self.targetCurrency = CurrencyDTO(target_currency).to_dict()
        self.rate = rate
        self.amount = amount
        self.converted_amount = converted_amount

    def to_dict(self) -> dict:
        return self.__dict__
