from . import impl

dict_to_readonly_object = impl.DictionaryObjectConverter(readonly=True).dict_to_object
dict_to_writable_object = impl.DictionaryObjectConverter().dict_to_object
object_to_dict = impl.DictionaryObjectConverter().object_to_dict
