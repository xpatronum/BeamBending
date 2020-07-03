from pathlib import Path
from abc import ABC, abstractmethod


class Writer(ABC):

    def __init__(self, directory=None, filename=None):
        self._directory = Path(directory)
        if not self._directory.exists():
            self._directory.mkdir(parents=True)
        self._filename = Path(filename) if filename is not None else None
        self._filepath = self()

    def __call__(self):
        try:
            return Path(self._directory / self._filename)
        except TypeError:
            return None

    @property
    def directory(self):
        return str(self._directory)

    @directory.setter
    def directory(self, arg):
        self._directory = Path(arg)
        self._filepath = self()

    @property
    def filename(self):
        return str(self._filename)

    @filename.setter
    def filename(self, arg):
        self._filename = Path(arg)
        self._filepath = self()

    @property
    def filepath(self):
        return str(self._filepath)

    @filepath.setter
    def filepath(self, arg):
        fpath = Path(arg)
        self.directory = fpath.parent
        self.filename = fpath.name
        self._filepath = self()

    @abstractmethod
    def write(self, data, **kwargs):
        pass
