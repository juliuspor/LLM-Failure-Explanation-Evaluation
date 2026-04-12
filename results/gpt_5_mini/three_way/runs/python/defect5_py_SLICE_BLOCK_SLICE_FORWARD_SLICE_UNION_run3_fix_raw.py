@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is not None:
        inferred_type = type(array)
    elif element is not None:
        inferred_type = type(element)
    else:
        inferred_type = object

    new_list = ArrayUtils._copy_list_grow1(array, inferred_type)
    new_list[len(new_list) - 1] = element

    if expected_type is not None:
        # If array is an actual list, check its elements' runtime types against expected_type
        # Allow None elements; only validate non-None values.
        if array is not None:
            for i, v in enumerate(array):
                if v is not None and not isinstance(v, expected_type):
                    raise TypeError(
                        f"Cannot cast list element at index {i} of type {type(v).__name__} to {expected_type.__name__}"
                    )
        # Check the new element as well
        if element is not None and not isinstance(element, expected_type):
            raise TypeError(
                f"Cannot cast element of type {type(element).__name__} to {expected_type.__name__}"
            )

    return new_list