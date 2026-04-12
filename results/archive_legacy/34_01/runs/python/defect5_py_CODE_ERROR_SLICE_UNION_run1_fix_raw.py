@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if expected_type is not None:
        inferred_type = expected_type
    elif array is not None:
        if len(array) > 0 and array[0] is not None:
            inferred_type = type(array[0])
        else:
            inferred_type = object
    elif element is not None:
        inferred_type = type(element)
    else:
        inferred_type = object

    if expected_type is not None and array is not None:
        for i, item in enumerate(array):
            if item is None:
                continue
            if not isinstance(item, expected_type):
                raise TypeError(
                    f"Cannot cast list element at index {i} of type {type(item).__name__} to {expected_type.__name__}"
                )

    new_list = ArrayUtils._copy_list_grow1(array, inferred_type)
    new_list[len(new_list) - 1] = element

    return new_list