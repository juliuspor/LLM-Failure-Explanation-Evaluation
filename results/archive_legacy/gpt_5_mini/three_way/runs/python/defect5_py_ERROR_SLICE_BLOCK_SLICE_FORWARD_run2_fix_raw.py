@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is not None:
        inferred_type = type(array)
    elif element is not None:
        inferred_type = type(element)
    else:
        inferred_type = object
    new_list = ArrayUtils._copy_list_grow1(array, inferred_type)
    new_list[len(new_list) - 1] = element
    if expected_type is not None:
        def try_convert(val):
            if val is None:
                return None
            if isinstance(val, expected_type):
                return val
            try:
                return expected_type(val)
            except Exception:
                raise TypeError(f"Cannot convert element of type {type(val).__name__} to {expected_type.__name__}")
        for i, v in enumerate(new_list):
            new_list[i] = try_convert(v)
    return new_list