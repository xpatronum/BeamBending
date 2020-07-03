from stream.reader.Reader import Reader as Base
from pathlib import Path
import json


class ReaderJson(Base):

    def __init__(self, directory, filename, inplace=False, **params):
        """
        :param directory: Path to current working directory
        :param filename: File to open
        """
        super(ReaderJson, self).__init__(directory=directory, filename=filename)

        self.data = None if not inplace else self.read(**params)

    @classmethod
    def fromFile(cls, filepath=None, inplace=False, **params):
        fp = Path(filepath)
        return cls(fp.parent, fp.name, inplace, **params)

    def read(self, **params):
        if not self.filepath.exists():
            raise FileNotFoundError(str(self.filepath))
        with open(str(self.filepath), encoding='utf-8') as f:
            return json.load(f)

    def __call__(self, key):
        if key not in dir(self):
            raise KeyError('{:s} is not a member of class {:s}'.format(str(key), str(self)))
        return getattr(self, key)

    def __str__(self):
        return str(self.__class__)
