@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if expected_type is not None:
        inferred_type = expected_type
    elif array is not None:
        inferred_type = object
        for e in array:
            if e is not None:
                inferred_type = type(e)
                break
    elif element is not None:
        inferred_type = type(element)
    else:
        inferred_type = object

    if expected_type is not None and element is not None:
        if not isinstance(element, expected_type):
            raise TypeError(
                f"Cannot cast element of type {type(element).__name__} to {expected_type.__name__}"
            )

    new_list = ArrayUtils._copy_list_grow1(array, inferred_type)
    new_list[len(new_list) - 1] = element
    return new_list