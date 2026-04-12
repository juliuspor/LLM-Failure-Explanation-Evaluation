@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is not None:
        if len(array) > 0:
            inferred_type = expected_type or (type(array[0]) if array[0] is not None else object)
        else:
            inferred_type = expected_type or object
    elif element is not None:
        inferred_type = expected_type or type(element)
    else:
        inferred_type = expected_type or object

    new_list = ArrayUtils._copy_list_grow1(array, inferred_type)
    new_list[len(new_list) - 1] = element

    return new_list