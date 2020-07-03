from stream.reader.Reader import Reader as Base
import pandas as pd
from pathlib import Path


class ReaderCsv(Base):

    def __init__(self, directory, filename, inplace=False, **params):
        super(ReaderCsv, self).__init__(directory=directory, filename=filename)
        self.data = None if not inplace else self.read(**params)

    @classmethod
    def fromFile(cls, filepath=None):
        fp = Path(filepath)
        return cls(fp.parent, fp.name)

    def read(self, **params):
        '''
        :param separator: separator that is used in .csv file
        :return: Pandas.DataFrame
        '''
        separator = params.get('separator', ',')
        encoding = params.get('encoding', 'utf-8-sig')
        fp = str(self.filepath)
        if fp.endswith('.csv'):
            return pd.read_csv(fp, sep=separator, encoding=encoding)
        if fp.endswith('.xlsx') or fp.endswith('.xls'):
            return pd.read_excel(fp).to_csv(sep=separator, encoding=encoding)
