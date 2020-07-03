from stream.reader.Reader import Reader as Parent


class ReaderConsole(Parent):

    def __init__(self):
        super(ReaderConsole, self).__init__()

    def read(self, **kwargs):
        pass
