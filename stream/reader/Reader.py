from abc import ABC, abstractmethod
from pathlib import Path


class Reader(ABC):

    class Wrapper:

        def __init__(self, directory=None, filename=None):
            self.directory = directory
            self.filename = filename

    def __init__(self, directory=None, filename=None):
        self.wrapper = Reader.Wrapper(Path(directory), Path(filename))

    @property
    def directory(self):
        return self.wrapper.directory

    @directory.setter
    def directory(self, arg):
        self.wrapper.directory = Path(arg)

    @property
    def filename(self):
        return self.wrapper.filename

    @filename.setter
    def filename(self, arg):
        self.wrapper.filename = Path(arg)

    @property
    def filepath(self):
        return self.directory / self.filename

    @filepath.setter
    def filepath(self, arg):
        arg = Path(arg)
        self.directory = arg.parent
        self.filename = arg.name

    @abstractmethod
    def read(self, **kwargs):
        pass

