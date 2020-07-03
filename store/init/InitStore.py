from store.Store import IStore as Base
from stream import ReaderJson
from pathlib import Path
import copy
import os


class InitStore(Base):

    __UNK_KEY__ = 'UNK_KEY'
    __UNK_VALUE__ = 'UNK_VALUE'

    inst = None

    class Wrapper:

        def __init__(self):
            self.data = {}

    @staticmethod
    def instance():
        """ Static access method. """
        if InitStore.inst is None:
            InitStore()

        return InitStore.inst

    @property
    def data(self):
        return self.wrapper.data

    def __init__(self):

        if InitStore.inst is not None:
            raise Exception("This class is a singleton!")
        else:
            InitStore.inst = self
        super(InitStore, self).__init__()
        data = ReaderJson.fromFile(str(Path(os.environ['ROOT']) / 'init.json')).read()
        self.wrapper = InitStore.Wrapper()
        self.data['E'] = float(data['E'])
        self.data['I'] = float(data['I'])
        self.data['L'] = float(data['L'])
        self.data['K'] = float(data['K'])
        self.data['P'] = float(data['P'])
        self.data['Mg'] = float(data['Mg'])
        self.data['Q'] = float(data['Q'])
        self.data['points'] = [float(p) for p in data['points']]
        self.data['version'] = data['version']
        self.data['output'] = data['output']
        del data

    def query(self, key, **params):
        kk = self.__UNK_KEY__ if key not in self.data else key
        return self.data[kk]

    def put(self, key, value, **params):
        kk = self.__UNK_KEY__ if key is None or value is None else key
        vv = self.__UNK_VALUE__ if key is None or value is None else value
        self.data[kk] = vv