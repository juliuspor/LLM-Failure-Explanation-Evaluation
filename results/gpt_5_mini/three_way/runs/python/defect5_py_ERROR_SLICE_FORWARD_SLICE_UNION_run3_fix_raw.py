@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is not None:
        inferred_type = type(array)
    elif element is not None:
        inferred_type = type(element)
    else:
        inferred_type = object

    # Create a new list grown by one
    new_list = ArrayUtils._copy_list_grow1(array, expected_type if expected_type is not None else inferred_type)
    new_list[len(new_list) - 1] = element

    # If expected_type is given, ensure element is compatible with it
    if expected_type is not None and element is not None:
        if not isinstance(element, expected_type):
            raise TypeError(
                f"Element of type {type(element).__name__} cannot be added to list of {expected_type.__name__}"
            )

    return new_list