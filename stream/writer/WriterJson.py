from stream.writer.Writer import Writer as Parent
import json

import os


class WriterJson(Parent):

    def __init__(self, directory, filename):
        super().__init__(directory=directory, filename=filename)

    def write(self, data):
        with open(self.filepath, 'w') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        f.close()
