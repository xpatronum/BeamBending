from tool.fcall import ICallable
import math


class Polynomial:

    class Caller:

        def __init__(self):
            pass

        def __call__(self, x, *args, **kwargs):
            n = kwargs.get('n', 1)
            return x ** n / math.factorial(n)

    def __init__(self):
        self.caller = Polynomial.Caller()
        self.c = ICallable(f=self.caller)

    def __call__(self, x, *args, **kwargs):
        return self.caller(x, *args, **kwargs)