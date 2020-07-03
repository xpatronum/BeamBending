from plot.IPlot import Plot as Base
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from pathlib import Path


class Plot(Base):

    class ValuePosition:

        ABOVE = 0,
        BELOW = 1,
        OFF = 2

    def __init__(self, data=None, params=Base.params):
        super(Plot, self).__init__(data=data, params=params)

        self.canvas, self.axes = plt.subplots(figsize=params['figure.figsize'])
        self.rotation = None
        self.position = Plot.ValuePosition.ABOVE
        sns.set(rc=self.params,
                style='white'
        )

    def setRotation(self, angle):
        self.rotation = angle

    def compile(self, it, xs, **params):
        assert len(it) == len(xs)
        data = pd.DataFrame(columns=['x'])
        n = params.get('n', 1000)
        for i, iCall in enumerate(it):
            s, e = xs[i]
            step = (e - s) / n
            xxs = np.array([0.0] * n)
            yys = np.array([0.0] * n)
            for j in range(n):
                xxs[j] = (s + step * j)
                yys[j] = iCall(xxs[j])
            di = pd.DataFrame({'x': xxs, str(i): yys})
            data = pd.merge(data, di, on='x', how='outer')
        subscriptions = params.get('subscriptions', [str(i) for i in list(np.arange(len(it)))])
        assert len(subscriptions) == len(xs)
        data.columns = ['x'] + subscriptions
        self.wrapper.data = pd.melt(data, id_vars=['x'], var_name='-', value_name='F = F(x)')
        return self

    def rotate(self, p):
        if self.rotation:
            for tick in p.get_xticklabels():
                tick.set_rotation(self.rotation)
        return p

    def view(self, p):
        return p

    def subscription(self, p):
        '''
        :param p: sns.barplot(...options)
        :return: sns.barplot(...options)
        '''
        if self.title is not None:
            p.set_title(self.title)
        if self.xTitle is not None:
            p.set_xlabel(self.xTitle)
        if self.yTitle is not None:
            p.set_ylabel(self.yTitle)
        return p

    def show(self):
        '''
        :return:
        '''
        if self.wrapper.data is None:
            raise ValueError('Plot is not compiled before plotting (calling plot.show())')
        plt.rcParams.update(self.params)
        sns.lineplot(x='x', y='F = F(x)', data=self.wrapper.data, hue='-', ax=self.axes)
        p = self.rotate(self.axes)
        p = self.view(p)
        p = self.subscription(p)
        plt.show(block=False)
        self.axes = p
        return self

    def save(self, filepath, dpi=250, extension='pdf'):
        self.canvas.savefig(str(Path(filepath + '.' + extension)), dpi=dpi)
        return self

    def close(self):
        plt.close(self.axes.get_figure())

    def __repr__(self):
        return 'Plot({!r})'.format(self.data)
