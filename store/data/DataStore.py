from store.Store import IStore as Base


class DataStore(Base):

    __UNK_KEY__ = 'UNK_KEY'
    __UNK_VALUE__ = 'UNK_VALUE'

    inst = None

    @staticmethod
    def instance():
        """ Static access method. """
        if DataStore.inst is None:
            DataStore()
        return DataStore.inst

    def __init__(self):
        if DataStore.inst is not None:
            raise Exception("This class is a singleton!")
        else:
            DataStore.inst = self

        super(DataStore, self).__init__()
        self.data = {}

    def query(self, key, **params):
        kk = self.__UNK_KEY__ if key not in self.data else key
        return self.data[kk]

    def put(self, key, value, **params):
        kk = self.__UNK_KEY__ if key is None or value is None else key
        vv = self.__UNK_VALUE__ if key is None or value is None else value
        self.data[kk] = vv
