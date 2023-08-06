from types import SimpleNamespace
from copy import deepcopy
from . import type as ty


class DictionaryToObjectConverter:
    def __init__(self, readonly):
        self.obj_class = ty.ReadOnlyObject if readonly else ty.WritableObject

    def __call__(self, dct: dict):
        copied: dict = deepcopy(dct)
        for key, value in copied.items():
            if isinstance(value, dict):
                copied[key] = self(value)
        return self.obj_class(**copied)


class DictionaryToReadOnlyObjectConverter(DictionaryToObjectConverter):
    def __init__(self):
        super().__init__(True)


class DictionaryToWritableObjectConverter(DictionaryToObjectConverter):
    def __init__(self):
        super().__init__(False)


class ObjectToDictionaryConverter:
    def __call__(self, obj) -> dict:
        copied: dict = deepcopy(obj.__dict__)
        for key, value in copied.items():
            if isinstance(value, SimpleNamespace):
                copied[key] = self(value)
        return copied
