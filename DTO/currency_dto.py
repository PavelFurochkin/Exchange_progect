
class CurrencyDTO:
    """Создает DTO для конкретной валюты

    Attributes
    ----------
    id
        ID валюты
    name
        FullName валюты
    code
        Code валюты
    sign
        Sign валюты

    Methods
    -------
    to_dict()
        Возвращает представление валюты в словаре
    """
    def __init__(self, data: tuple):
        self.id = data[0]
        self.name = data[1]
        self.code = data[2]
        self.sign = data[3]

    def to_dict(self) -> dict:
        return self.__dict__
