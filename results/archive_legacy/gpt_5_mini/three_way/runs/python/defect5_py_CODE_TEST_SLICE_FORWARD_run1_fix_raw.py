@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if expected_type is not None:
        inferred_type = expected_type
    elif element is not None:
        inferred_type = type(element)
    elif array is not None and len(array) > 0:
        first_non_none = next((x for x in array if x is not None), None)
        inferred_type = type(first_non_none) if first_non_none is not None else object
    else:
        inferred_type = object

    if expected_type is not None and element is not None and not isinstance(element, expected_type):
        raise TypeError(
            f"Cannot add element of type {type(element).__name__} to list of {expected_type.__name__}"
        )

    new_list = ArrayUtils._copy_list_grow1(array, inferred_type)
    new_list[len(new_list) - 1] = element
    return new_list