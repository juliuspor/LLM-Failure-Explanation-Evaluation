@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if expected_type is not None:
        inferred_type = expected_type
    elif array is not None:
        if len(array) > 0:
            first_non_none = None
            for it in array:
                if it is not None:
                    first_non_none = type(it)
                    break
            inferred_type = first_non_none if first_non_none is not None else object
        else:
            inferred_type = object
    elif element is not None:
        inferred_type = type(element)
    else:
        inferred_type = object

    new_list = ArrayUtils._copy_list_grow1(array, inferred_type)
    new_list[len(new_list) - 1] = element

    if expected_type is not None:
        if element is not None and not isinstance(element, expected_type):
            raise TypeError(
                f"Cannot cast element of type {type(element).__name__} to {expected_type.__name__}"
            )
        if array is not None and len(array) > 0:
            for i, it in enumerate(array):
                if it is not None and not isinstance(it, expected_type):
                    raise TypeError(
                        f"Array element at index {i} of type {type(it).__name__} cannot be cast to {expected_type.__name__}"
                    )
    return new_list