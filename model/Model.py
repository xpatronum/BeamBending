import numpy as np
from store import InitStore
from tool.fcall.math import Polynomial
from tool.fcall import ICallable
from plot.fun import Plot
from pathlib import Path
import math


class Model:

    class ToolWrapper:

        def __init__(self, context):
            self.context = context

            self.EI = context.params['E'] * context.params['I']
            self.L = context.params['L']
            self.K = context.params['K']
            self.Q = context.params['Q']
            self.P = context.params['P']
            self.M = context.params['Mg']


        @property
        def constants(self):
            return tuple([self.EI, self.L, self.K, self.Q, self.P, self.M])

        @property
        def points(self):
            return self.context.params['points']

        def __call__(self, x, *args, **kwargs):
            unpack = kwargs.get('unpack', False)
            query = getattr(self.context, x)
            return query if not unpack else tuple(query)

    def __init__(self, n):
        self.params = InitStore.instance().data
        self.lhs = np.zeros(shape=(n, n))
        self.rhs = np.zeros(shape=(n, 1))
        self.solution = None
        self.wrapper = Model.ToolWrapper(self)

    @property
    def c(self):
        return self.params

    @classmethod
    def build(cls, size):
        return cls(size)

    def compile(self):
        EI, L, K, Q, P, M = self.wrapper.constants
        pts = self.wrapper.points
        dif = lambda x, y, r: float((x - y) ** r) / math.factorial(r)
        # Left hand side of the system of linear equations
        self.lhs[0] = [dif(L, pts[2], 1) / EI, dif(L, pts[4], 1) / EI, dif(L, pts[5], 1) / EI, 0, 0]
        self.lhs[1] = [1.0 / EI, 1.0 / EI, 1.0 / EI, 0, 0]
        self.lhs[2] = [0, 0, 0, pts[2] / EI, 1.0 / EI]
        self.lhs[3] = [dif(pts[4], pts[2], 3) / EI, 0, 0, pts[4] / EI, 1.0 / EI]
        self.lhs[4] = [K / EI * dif(pts[5], pts[2], 3), K / EI * dif(pts[5], pts[4], 3), K / EI, K / EI * pts[5], K / EI]
        # Right hand side of the system of linear equations
        self.rhs[0] = 1.0 / EI * (Q * dif(L, pts[6], 2) + P * dif(L, pts[1], 1) + M)
        self.rhs[1] = 1.0 / EI * (Q * dif(L, pts[6], 1)) + P
        self.rhs[2] = 1.0 / EI * (P * dif(pts[2], pts[1], 2))
        self.rhs[3] = 1.0 / EI * (P * dif(pts[4], pts[1], 2) + M * dif(pts[4], pts[3], 2))
        self.rhs[4] = K / EI * (P * dif(pts[5], pts[1], 2) + M * dif(pts[5], pts[3], 2))
        return self

    def solve(self):
        self.solution = np.linalg.solve(self.lhs, self.rhs)
        return self

    def save(self, directory, ext='pdf'):
        plot = Plot()
        plot = plot.compile(it=[self.shift, self.angle, self.moment, self.force],
                            xs=[(0.0, 20.0), (0.0, 20.0), (0.0, 20.0), (0.0, 20.0)],
                            subscriptions=['Shift', 'Angle', 'Moment', 'Force'])
        plot = plot.show()
        plot = plot.save(filepath=str(Path(directory) / 'graph'), extension=ext)
        plot.close()
        return self

    def close(self):
        pass

    def shift(self, x):
        EI, _, _, Q, P, M = self.wrapper.constants
        ps = self.wrapper.points
        p = Polynomial()
        h = ICallable(f=np.heaviside)
        R2, R4, R5, angle, sh = self.wrapper('solution', unpack=True)
        return \
            1.0 / EI * \
            Q * p(x - ps[6], n=4) * h(x - ps[6], 0) + \
            P * p(x - ps[1], n=2) * h(x - ps[1], 0) - \
            R2 * p(x - ps[2], n=3) * h(x - ps[2], 0) - \
            R4 * p(x - ps[4], n=3) * h(x - ps[4], 0) - \
            R5 * p(x - ps[5], n=3) * h(x - ps[5], 0) + \
            M * p(x - ps[3], n=2) * h(x - ps[3], 0) + \
            angle * x + \
            sh

    def angle(self, x):
        EI, _, _, Q, P, M = self.wrapper.constants
        ps = self.wrapper.points
        p = Polynomial()
        h = ICallable(f=np.heaviside)
        R2, R4, R5, angle, _ = self.wrapper('solution', unpack=True)
        return \
            1.0 / EI * \
            Q * p(x - ps[6], n=3) * h(x - ps[6], 0) + \
            P * p(x - ps[1], n=2) * h(x - ps[1], 0) - \
            R2 * p(x - ps[2], n=2) * h(x - ps[2], 0) - \
            R4 * p(x - ps[4], n=2) * h(x - ps[4], 0) - \
            R5 * p(x - ps[5], n=2) * h(x - ps[5], 0) + \
            M * p(x - ps[3], n=1) * h(x - ps[3], 0) + \
            angle

    def moment(self, x):
        EI, _, _, Q, P, M = self.wrapper.constants
        ps = self.wrapper.points
        p = Polynomial()
        h = ICallable(f=np.heaviside)
        R2, R4, R5, _, _ = self.wrapper('solution', unpack=True)
        return 1.0 / EI * \
            Q * p(x - ps[6], n=2) * h(x - ps[6], 0) + \
            P * p(x - ps[1], n=1) * h(x - ps[1], 0) - \
            R2 * p(x - ps[2], n=1) * h(x - ps[2], 0) - \
            R4 * p(x - ps[4], n=1) * h(x - ps[4], 0) - \
            R5 * p(x - ps[5], n=1) * h(x - ps[5], 0) + \
            M * h(x - ps[3], 0)

    def force(self, x):
        EI, _, _, Q, P, _ = self.wrapper.constants
        ps = self.wrapper.points
        p = Polynomial()
        h = ICallable(f=np.heaviside)
        R2, R4, R5, _, _ = self.wrapper('solution', unpack=True)
        return 1.0 / EI * \
            Q * p(x - ps[6], n=1) * h(x - ps[6], 0) + \
            P * h(x - ps[1], 0) - \
            R2 * h(x - ps[2], 0) - \
            R4 * h(x - ps[4], 0) - \
            R5 * h(x - ps[5], 0)
