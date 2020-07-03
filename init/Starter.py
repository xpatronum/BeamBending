import os
from pathlib import Path
from store import DataStore, InitStore


class Starter:

    inst = None
    __version__ = 'VERSION'

    @staticmethod
    def init(root=os.environ.get('ROOT', str(Path(os.getcwd())))):
        """ Static access method. """
        if Starter.inst is None:
            Starter(root)

    @staticmethod
    def activated():
        return Starter.inst is not None

    def onInit(self, root):
        os.environ['ROOT'] = str(root)

    def __init__(self, root):
        """ Virtually private constructor. """
        Starter.inst = self
        self.onInit(root)
        self.initStore = InitStore.instance()
        self.dataStore = DataStore.instance()
