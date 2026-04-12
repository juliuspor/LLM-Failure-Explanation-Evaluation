@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is not None and len(array) > 0:
        inferred_type = None
        for v in array:
            if v is not None:
                inferred_type = type(v)
                break
        if inferred_type is None and element is not None:
            inferred_type = type(element)
        elif inferred_type is None:
            inferred_type = expected_type if expected_type is not None else object
    elif element is not None:
        inferred_type = type(element)
    else:
        inferred_type = expected_type if expected_type is not None else object

    if expected_type is not None:
        if array is not None:
            for v in array:
                if v is not None and not isinstance(v, expected_type):
                    raise TypeError(f"Cannot cast {type(v).__name__} list to {expected_type.__name__} list")
        if element is not None and not isinstance(element, expected_type):
            raise TypeError(f"Cannot cast {type(element).__name__} to {expected_type.__name__}")

    new_list = ArrayUtils._copy_list_grow1(array, inferred_type)
    new_list[len(new_list) - 1] = element
    return new_list