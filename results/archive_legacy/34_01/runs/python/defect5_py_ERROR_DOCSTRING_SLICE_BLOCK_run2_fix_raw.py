@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is not None:
        inferred_type = None
        for e in array:
            if e is not None:
                inferred_type = type(e)
                break
        if inferred_type is None:
            inferred_type = object
    elif element is not None:
        inferred_type = type(element)
    else:
        inferred_type = object

    new_list = ArrayUtils._copy_list_grow1(array, inferred_type)
    new_list[len(new_list) - 1] = element

    if expected_type is not None:
        if inferred_type == object and array is not None:
            for i, e in enumerate(array):
                if e is not None and not isinstance(e, expected_type):
                    raise TypeError(f"Element at index {i} is of type {type(e).__name__}; cannot cast to {expected_type.__name__}")
        elif inferred_type is not object and not issubclass(inferred_type, expected_type):
            raise TypeError(
                f"Cannot cast {inferred_type.__name__} list to {expected_type.__name__} list (ClassCastException)"
            )
    return new_list