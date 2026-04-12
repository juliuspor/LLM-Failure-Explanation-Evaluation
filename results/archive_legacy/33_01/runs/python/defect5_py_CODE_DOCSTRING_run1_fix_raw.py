@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is not None and len(array) > 0:
        inferred_type = type(array[0])
    elif element is not None:
        inferred_type = type(element)
    else:
        inferred_type = object

    new_list = ArrayUtils._copy_list_grow1(array, inferred_type)
    new_list[-1] = element

    if expected_type is not None:
        if element is not None and not isinstance(element, expected_type):
            raise TypeError(
                f"Cannot cast element of type {type(element).__name__} to {expected_type.__name__}"
            )
        if array is not None:
            for i, e in enumerate(array):
                if e is not None and not isinstance(e, expected_type):
                    raise TypeError(
                        f"Cannot cast array element at index {i} of type {type(e).__name__} to {expected_type.__name__}"
                    )

    return new_list