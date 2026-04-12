@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if expected_type is not None:
        inferred_type = expected_type
    else:
        if array is not None:
            # infer from array contents if possible, else from list type
            if len(array) > 0 and array[0] is not None:
                inferred_type = type(array[0])
            else:
                inferred_type = type(array) if array is not None else (type(element) if element is not None else object)
        elif element is not None:
            inferred_type = type(element)
        else:
            inferred_type = object

    # If array provided, ensure its elements are compatible with expected_type (if given)
    if array is not None and expected_type is not None:
        for i, it in enumerate(array):
            if it is not None and not isinstance(it, expected_type):
                raise TypeError(f"Cannot cast element at index {i} of type {type(it).__name__} to {expected_type.__name__}")

    # Build new list
    if array is not None:
        new_list = array.copy()
        new_list.append(None)
    else:
        new_list = [None]

    # Assign element (no runtime cast in Python, but simulate type check)
    if expected_type is not None and element is not None and not isinstance(element, expected_type):
        raise TypeError(f"Cannot cast element of type {type(element).__name__} to {expected_type.__name__}")

    new_list[len(new_list) - 1] = element
    return new_list