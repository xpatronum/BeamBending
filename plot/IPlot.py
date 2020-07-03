from abc import ABC, abstractmethod
import matplotlib.pyplot as plt
import seaborn as sns


class Plot(ABC):
    '''
    Interface for convenient plotting using "Seaborn" and "Matplotlib".
    This is just an API for convenience.
    '''

    class Wrapper:
        
        def __init__(self, data=None):
            self.data = data

    params = {
        'figure.figsize': (11.7, 8.27),
        'font.size': 9,
        'axes.titlesize': 20,
        'axes.labelsize': 12.5,
        'font.family': 'serif',
    }

    pallets = {
        "blue": sns.color_palette("GnBu_d"),
        "green": sns.cubehelix_palette(8, start=2, rot=0, dark=0, light=.95, reverse=True),
        "purple": sns.dark_palette("purple"),
        "navy": sns.light_palette("navy", reverse=True)
    }

    def __init__(self, data=None, params=None):
        '''
        :param data: [optional]
        '''
        self.wrapper = Plot.Wrapper(data)
        self.palette = self.pallets['blue']
        self.title = None

        self.params = params if params is not None else self.params
        plt.rcParams.update(params)

        self.xTitle = None
        self.yTitle = None

    @property
    def data(self):
        return self.wrapper.data

    @data.setter
    def data(self, value):
        del self.wrapper.data
        self.wrapper.data = value

    def setPalette(self, palette):
        self.palette = palette
        return self

    def setTitle(self, title):
        self.title = title
        return self

    def setConfig(self, config):
        del self.params
        self.params = config
        return self

    def setXTitle(self, xTitle):
        self.xTitle = xTitle
        return self

    def setYTitle(self, yTitle):
        self.yTitle = yTitle
        return self

    def setLabelSize(self, size):
        self.params['axes.labelsize'] = size
        return self

    @abstractmethod
    def compile(self, it, xs, **params):
        '''
        :return: Self object. For chaining method calls...
        '''
        pass

    @abstractmethod
    def show(self):
        '''
        :return: Self object. For chaining method calls...
        '''
        pass

    @abstractmethod
    def save(self, filepath, dpi=250, extension='pdf'):
        '''
        :return: Self object. For chaining method calls...
        '''
        pass

    @abstractmethod
    def close(self):
        '''
        :return: Nothing. End of chain call
        '''
        pass

    def __repr__(self):
        return self.data
