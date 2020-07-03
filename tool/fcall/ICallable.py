from abc import ABC


class ICallable(ABC):

    def __init__(self, f=None, tracker=-1):
        self.f = f
        self.tracker = tracker
        self.metainfo = ['f', 'tracker']

    def __call__(self, x, *args, **kwargs):
        return self.f(x, *args, **kwargs)

    def __hash__(self):
        return sum([hash(getattr(self, x)) for x in self.metainfo])

    def __eq__(self, other):
        return id(self) == id(other) and self.tracker == other.tracker
