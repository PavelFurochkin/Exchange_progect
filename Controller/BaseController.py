from abc import ABC, abstractmethod

class BaseController(ABC):

    @abstractmethod
    def do_GET(self):
        pass

    @abstractmethod
    def do_Post(self):
        pass
