@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is not None:
        inferred_type = type(array)
    elif element is not None:
        inferred_type = type(element)
    elif expected_type is not None:
        inferred_type = expected_type
    else:
        inferred_type = object

    new_list = ArrayUtils._copy_list_grow1(array, inferred_type)
    new_list[len(new_list) - 1] = element

    if expected_type is not None:
        # Only raise if the provided element is incompatible with expected_type
        if element is not None and not isinstance(element, expected_type):
            raise TypeError(
                f"Element of type {type(element).__name__} cannot be added to list of {expected_type.__name__}"
            )

    return new_list