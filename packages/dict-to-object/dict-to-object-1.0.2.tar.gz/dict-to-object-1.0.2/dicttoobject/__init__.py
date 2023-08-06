from . import impl


DoNotWriteError = impl.DoNotWriteError
dict_to_readonly_object = impl.DictionaryToObjectConverter(readonly=True)
dict_to_writable_object = impl.DictionaryToObjectConverter(readonly=False)
object_to_dict = impl.ObjectToDictionaryConverter()
