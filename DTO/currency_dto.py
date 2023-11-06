
class CurrencyDTO:
    def __init__(self, data: tuple):
        self.id = data[0]
        self.name = data[1]
        self.code = data[2]
        self.sign = data[3]

    def to_dict(self):
        return self.__dict__
