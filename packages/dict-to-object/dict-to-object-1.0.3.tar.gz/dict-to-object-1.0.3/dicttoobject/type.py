from types import SimpleNamespace
from . import error


class WritableObject(SimpleNamespace):
    pass        


class ReadOnlyObject(SimpleNamespace):
    def __setattr__(self, attr_name, attr_value):
        raise error.DoNotWriteError(attr_name, attr_value)
