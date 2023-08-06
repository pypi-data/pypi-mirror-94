from types import SimpleNamespace
from copy import deepcopy


class DoNotWriteError(Exception):
    def __init__(self, attr_name: str, attr_value):
        super().__init__(f'do not write to read only attribute [{attr_name}], value [{attr_value}].')
        self.attr_name = attr_name
        self.attr_value = deepcopy(attr_value)


class WritableObject(SimpleNamespace):
    pass        


class ReadOnlyObject(SimpleNamespace):
    def __setattr__(self, attr_name, attr_value):
        raise DoNotWriteError(attr_name, attr_value)


class DictionaryToObjectConverter:
    def __init__(self, readonly):
        self.obj_class = ReadOnlyObject if readonly else WritableObject

    def __call__(self, dct: dict):
        copied: dict = deepcopy(dct)
        for key, value in copied.items():
            if isinstance(value, dict):
                copied[key] = self(value)
        return self.obj_class(**copied)


class ObjectToDictionaryConverter:
    def __call__(self, obj) -> dict:
        copied: dict = deepcopy(obj.__dict__)
        for key, value in copied.items():
            if isinstance(value, SimpleNamespace):
                copied[key] = self(value)
        return copied
