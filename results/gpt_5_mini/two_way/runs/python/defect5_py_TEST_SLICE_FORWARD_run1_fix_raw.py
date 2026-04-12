@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is not None:
        inferred_type = type(array)
    elif element is not None:
        inferred_type = type(element)
    else:
        inferred_type = object

    # Create new list (copy of array with one extra slot) or a new single-element list
    new_list = ArrayUtils._copy_list_grow1(array, inferred_type)
    new_list[len(new_list) - 1] = element

    # If expected_type is provided, perform type checks and simulate cast failure when appropriate
    if expected_type is not None:
        # If element is not None and not instance of expected_type -> TypeError
        if element is not None and not isinstance(element, expected_type):
            raise TypeError(
                f"Cannot cast element of type {type(element).__name__} to {expected_type.__name__}"
            )
        # If array provided, ensure existing non-None elements are instances of expected_type
        if array is not None:
            for i, item in enumerate(array):
                if item is not None and not isinstance(item, expected_type):
                    raise TypeError(
                        f"Cannot cast array element at index {i} of type {type(item).__name__} to {expected_type.__name__}"
                    )
        # If array is None and element is None, we cannot validate runtime types; allow and return list
    return new_list