from . import (
    error,
    type,
    converter
)


DoNotWriteError = error.DoNotWriteError

WritableObject = type.WritableObject
ReadOnlyObject = type.ReadOnlyObject

dict_to_readonly_object = converter.DictionaryToReadOnlyObjectConverter()
dict_to_writable_object = converter.DictionaryToWritableObjectConverter()
object_to_dict = converter.ObjectToDictionaryConverter()
