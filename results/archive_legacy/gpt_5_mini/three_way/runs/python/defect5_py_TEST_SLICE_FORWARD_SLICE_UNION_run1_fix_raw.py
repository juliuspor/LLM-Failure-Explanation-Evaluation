@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is not None:
        inferred_type = None
        for e in array:
            if e is not None:
                inferred_type = type(e)
                break
        if inferred_type is None:
            inferred_type = expected_type if expected_type is not None else object
    elif element is not None:
        inferred_type = type(element)
    else:
        inferred_type = expected_type if expected_type is not None else object
    if expected_type is not None:
        if array is not None:
            for i, e in enumerate(array):
                if e is not None and not isinstance(e, expected_type):
                    raise TypeError(
                        f"Cannot add element to list: element at index {i} is of type {type(e).__name__} which is not compatible with expected type {expected_type.__name__}"
                    )
        if element is not None and not isinstance(element, expected_type):
            raise TypeError(
                f"Element of type {type(element).__name__} is not compatible with expected type {expected_type.__name__}"
            )
    new_list = ArrayUtils._copy_list_grow1(array, inferred_type)
    new_list[len(new_list) - 1] = element
    return new_list