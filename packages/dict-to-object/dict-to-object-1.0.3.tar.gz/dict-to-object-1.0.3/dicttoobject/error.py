from copy import deepcopy


class DoNotWriteError(Exception):
    def __init__(self, attr_name: str, attr_value):
        super().__init__(f'do not write to read only attribute [{attr_name}], value [{attr_value}].')
        self.attr_name = attr_name
        self.attr_value = deepcopy(attr_value)
