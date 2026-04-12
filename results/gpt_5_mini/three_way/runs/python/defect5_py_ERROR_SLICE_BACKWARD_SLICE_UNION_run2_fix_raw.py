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
        # If array provided, ensure its existing elements are compatible with expected_type
        if array is not None:
            for i, item in enumerate(array):
                if item is not None and not isinstance(item, expected_type):
                    raise TypeError(
                        f"Cannot cast element at index {i} of type {type(item).__name__} to {expected_type.__name__}"
                    )
        # Check the new element
        if element is not None and not isinstance(element, expected_type):
            raise TypeError(
                f"Cannot cast element of type {type(element).__name__} to {expected_type.__name__}"
            )

    return new_list