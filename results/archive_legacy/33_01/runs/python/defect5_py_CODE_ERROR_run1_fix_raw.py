@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if expected_type is not None:
        inferred_type = expected_type
    elif element is not None:
        inferred_type = type(element)
    else:
        inferred_type = None
    if inferred_type is None and array is not None:
        for e in array:
            if e is not None:
                inferred_type = type(e)
                break
    if inferred_type is None:
        inferred_type = object
    if element is not None and expected_type is not None and not isinstance(element, expected_type):
        raise TypeError(
            f"Cannot cast element of type {type(element).__name__} to {expected_type.__name__}"
        )
    new_list = ArrayUtils._copy_list_grow1(array, inferred_type)
    new_list[len(new_list) - 1] = element
    return new_list