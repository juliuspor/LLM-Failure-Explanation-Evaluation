@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is not None:
        inferred_type = type(array)
    elif element is not None:
        inferred_type = type(element)
    else:
        inferred_type = object

    # If array is None, create a new list of size 1.
    new_list = ArrayUtils._copy_list_grow1(array, inferred_type)
    new_list[len(new_list) - 1] = element

    # If expected_type is provided, enforce that non-None elements are instances of it.
    if expected_type is not None:
        # If element is not None, ensure it's compatible with expected_type
        if element is not None and not isinstance(element, expected_type):
            raise TypeError(
                f"Cannot cast element of type {type(element).__name__} to {expected_type.__name__}"
            )
        # If array was provided, also ensure existing elements are compatible
        if array is not None:
            for i, item in enumerate(array):
                if item is not None and not isinstance(item, expected_type):
                    raise TypeError(
                        f"Cannot cast element at index {i} of type {type(item).__name__} to {expected_type.__name__}"
                    )
    return new_list