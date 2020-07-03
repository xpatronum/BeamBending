from init import Starter
from model import Model
from pathlib import Path
from store import InitStore
import os


if __name__ == '__main__':
    Starter.init()
    model = Model.build(size=5)
    model = model.compile()
    model = model.solve()
    model = model.save(Path(os.environ['ROOT']) / InitStore.instance().data['output']['directory'], ext='pdf')
    model.close()
