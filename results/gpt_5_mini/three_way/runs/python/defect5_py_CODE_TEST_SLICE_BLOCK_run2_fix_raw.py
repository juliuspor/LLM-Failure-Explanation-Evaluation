@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is not None and len(array) > 0:
        # infer from first element in array
        element_type = type(array[0])
    elif element is not None:
        element_type = type(element)
    elif expected_type is not None:
        element_type = expected_type
    else:
        element_type = object

    new_list = ArrayUtils._copy_list_grow1(array, element_type)
    new_list[len(new_list) - 1] = element

    # Only raise if we have concrete element type that definitely conflicts with expected_type
    if expected_type is not None:
        # If element is not None and its type is incompatible with expected_type, raise
        if element is not None and not issubclass(type(element), expected_type):
            raise TypeError(
                f"Cannot cast element of type {type(element).__name__} to {expected_type.__name__}"
            )
        # If array had elements and their type conflicts with expected_type, raise
        if array is not None and len(array) > 0:
            first_type = type(array[0])
            if not issubclass(first_type, expected_type):
                raise TypeError(
                    f"Cannot cast array elements of type {first_type.__name__} to {expected_type.__name__}"
                )
    return new_list