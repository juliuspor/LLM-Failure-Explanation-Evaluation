@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if expected_type is not None:
        inferred_type = expected_type
    else:
        inferred_type = object
        if array is not None and len(array) > 0:
            inferred_type = type(next((x for x in array if x is not None), array[0]))
        elif element is not None:
            inferred_type = type(element)
    new_list = ArrayUtils._copy_list_grow1(array, inferred_type)
    new_list[len(new_list) - 1] = element
    if expected_type is not None and element is not None and not isinstance(element, expected_type):
        raise TypeError(
            f"Cannot add element of type {type(element).__name__} to list of expected type {expected_type.__name__}"
        )
    return new_list