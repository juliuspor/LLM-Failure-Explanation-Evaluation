@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is not None and len(array) > 0:
        inferred_type = type(array[0])
    elif array is not None and len(array) == 0:
        # empty array: prefer expected_type, else element type, else object
        if expected_type is not None:
            inferred_type = expected_type
        elif element is not None:
            inferred_type = type(element)
        else:
            inferred_type = object
    elif element is not None:
        inferred_type = type(element)
    else:
        inferred_type = expected_type if expected_type is not None else object

    # If expected_type provided, validate element compatibility when element is not None
    if expected_type is not None and element is not None:
        if not isinstance(element, expected_type):
            raise TypeError(f"Element of type {type(element).__name__} cannot be added to list of {expected_type.__name__}")

    new_list = ArrayUtils._copy_list_grow1(array, inferred_type)
    new_list[len(new_list) - 1] = element

    return new_list