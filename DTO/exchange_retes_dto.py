from DTO.currency_dto import CurrencyDTO


class ExchangeRatesDTO:
    """Создает DTO для конкретной валюты

    Attributes
    ----------
    id
        ID обменного курса
    baseCurrency
        представление базовой валюты
    targetCurrency
        представление целевой валюты
    rate
        обменный курс пары

    Methods
    -------
    to_dict()
        Возвращает представление обменного курса в словаре
    """

    def __init__(self, id_rate: int, base_currency: tuple, target_currency: tuple, rate: float):
        self.id = id_rate
        self.baseCurrency = CurrencyDTO(base_currency).to_dict()
        self.targetCurrency = CurrencyDTO(target_currency).to_dict()
        self.rate = rate

    def to_dict(self) -> dict:
        return self.__dict__
