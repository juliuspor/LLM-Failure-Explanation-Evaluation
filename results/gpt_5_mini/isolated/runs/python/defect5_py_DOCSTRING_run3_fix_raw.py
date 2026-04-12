@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is not None and not isinstance(array, list):
        raise TypeError("array must be a list or None")

    # If expected_type provided, ensure element is compatible
    if expected_type is not None and element is not None and not isinstance(element, expected_type):
        raise TypeError(
            f"Cannot store element of type {type(element).__name__} in list of {expected_type.__name__}"
        )

    new_list = ArrayUtils._copy_list_grow1(array, expected_type)
    new_list[len(new_list) - 1] = element
    return new_list