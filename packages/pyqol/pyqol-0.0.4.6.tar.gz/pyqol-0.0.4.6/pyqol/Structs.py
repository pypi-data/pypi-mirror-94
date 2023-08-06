
from fastcore.all import store_attr
import functools
from fastcore.all import L
L = L

#? Dict, but cool
class Struct(object):
    def __init__(self, *args, **kwargs): 
        store_attr()
        for k, v in kwargs.items():
            vars(self)[k] = v
    def get(self, key):
        return vars(self).get(key)

class Registry():
    """Creates a registry of functions"""
    def __init__(self,):
        self.registry = dict()
    def register(self, f):
        self.registry[f.__name__] = f
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            f(*args, **kwargs)
        return wrapper
    def __getitem__(self, name):
        return self.registry[name]


import operator
class NaV():
    def __init__(self, message):
        store_attr()
        self.logs = L()
    def __str__(self):
        return f"Not a Value !\nMessage: {self.message}\n" + \
            ("Logs:\n" + "\n".join([f"Operation {k.__repr__()[19:-1]} with {v}" 
                for k, v in self.logs.items]) 
            if len(self.logs) > 0 else "")
    def __repr__(self):
        return self.__str__()
    @classmethod
    def consume(self, operator):
        def _(self, other):
            self.logs.append(L(operator, other))
            return self
        return _

for name in ["__add__", "__sub__", "__mul__", "__truediv__", "__floordiv__",
                "__mod__", "__pow__", "__rshift__", "__lshift__", "__and__",
                "__or__", "__xor__", "__LT__", "__GT__", "__LE__", "__GE__",
                "__EQ__", "__NE__", "__ISUB__", "__IADD__", "__IMUL__", "__IDIV__",
                "__IFLOORDIV__", "__IMOD__", "__IPOW__", "__IRSHIFT__", "__ILSHIFT__",
                "__IAND__", "__IOR__", "__IXOR__", "__NEG__", "__POS__", "__INVERT__"]:
    try:
        setattr(NaV, name, NaV.consume(getattr(operator, name.lower())))
    except:
        pass

