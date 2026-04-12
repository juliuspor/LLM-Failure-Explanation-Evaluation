@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is None:
        new_list: List[T] = [element]
    else:
        new_list = array.copy()
        new_list.append(element)

    # If expected_type provided, ensure all non-None elements are instances of expected_type.
    if expected_type is not None:
        for i, item in enumerate(new_list):
            if item is None:
                continue
            if not isinstance(item, expected_type):
                # Simulate Java ClassCastException behavior
                raise TypeError(
                    f"Cannot cast list element at index {i} of type {type(item).__name__} to {expected_type.__name__} "
                    f"(ClassCastException: {type(item).__name__} cannot be cast to {expected_type.__name__})"
                )
    return new_list