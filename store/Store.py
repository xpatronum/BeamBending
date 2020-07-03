from abc import ABC, abstractmethod


class IStore(ABC):

    def __init__(self):
        pass

    @abstractmethod
    def query(self, key, **params):
        pass

    @abstractmethod
    def put(self, key, value, **params):
        pass
