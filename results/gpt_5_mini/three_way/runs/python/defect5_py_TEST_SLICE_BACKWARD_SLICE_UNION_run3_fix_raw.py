@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if expected_type is not None:
        inferred_element_type = expected_type
    else:
        if array is not None and len(array) > 0:
            first = array[0]
            inferred_element_type = object if first is None else type(first)
        elif element is not None:
            inferred_element_type = type(element)
        else:
            inferred_element_type = object

    new_list = ArrayUtils._copy_list_grow1(array, inferred_element_type)
    new_list[len(new_list) - 1] = element

    # No TypeError should be raised when expected_type is provided; using expected_type as inferred type above
    return new_list