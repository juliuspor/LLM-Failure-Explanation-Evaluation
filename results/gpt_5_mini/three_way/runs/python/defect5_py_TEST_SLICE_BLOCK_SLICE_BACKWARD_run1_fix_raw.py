@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is not None:
        inferred_type = type(array)
    elif element is not None:
        inferred_type = type(element)
    else:
        inferred_type = object

    # If expected_type is provided and inferred_type is generic object,
    # prefer expected_type so we can create a list of that component type
    if expected_type is not None and inferred_type == object:
        inferred_type = expected_type

    new_list = ArrayUtils._copy_list_grow1(array, inferred_type)
    new_list[len(new_list) - 1] = element

    # If expected_type is provided, ensure compatibility if we have a concrete inferred_type
    if expected_type is not None:
        # If array existed, its type should be compatible with expected_type
        if array is not None and type(array) != expected_type and type(array) != object:
            raise TypeError(
                f"Cannot cast {type(array).__name__} list to {expected_type.__name__} list"
            )
        # Otherwise allow None-element lists or object-based lists to be considered as expected_type

    return new_list