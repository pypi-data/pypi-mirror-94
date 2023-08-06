# dict-to-object

```python
import dicttoobject

test_dict = {
    "key1": 1,
    "key2": {
        "key3": "value3"
    }
}

readonly_object = dicttoobject.dict_to_readonly_object(test_dict)
print(readonly_object)
# ReadOnlyObject(key1=1, key2=ReadOnlyObject(key3='value3'))

try:
    readonly_object.key2 = 2
except dicttoobject.DoNotWriteError as e:
    print(e.attr_name)
    # key2
    print(e.attr_value)
    # 2

writable_object = dicttoobject.dict_to_writable_object(test_dict)
print(writable_object)
# WritableObject(key1=1, key2=WritableObject(key3='value3'))

writable_object.key2.key3 = 3
print(writable_object.key2.key3)
# 3

writable_object.key4 = 4
print(writable_object.key4)
# 4

dict_from_readonly = dicttoobject.object_to_dict(readonly_object)
print(dict_from_readonly)
# {'key1': 1, 'key2': {'key3': 'value3'}}

dict_from_writable = dicttoobject.object_to_dict(writable_object)
print(dict_from_writable)
# {'key1': 1, 'key2': {'key3': 3}, 'key4': 4}
```