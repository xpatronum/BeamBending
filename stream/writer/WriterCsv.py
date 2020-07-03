from stream.writer.Writer import Writer as Base
from store import DataStore
from pathlib import Path


class WriterCsv(Base):

    def __init__(self, directory=None, filename=None):
        super(WriterCsv, self).__init__(directory, filename)
        self.initParams = DataStore.instance().query('INIT_PARAMS')

    @classmethod
    def fromFile(cls, filepath=None):
        fp = Path(filepath)
        return cls(fp.parent, fp.name)

    def write(self, data, **params):
        '''
        :param data: Pandas.DataFrame
        :return:
        '''
        encoding = params.get('encoding', 'utf-8-sig')
        separator = params.get('separator', self.initParams.separator)
        index = params.get('index', False)
        data.to_csv(self.filepath, encoding=encoding, sep=separator, index=index)
