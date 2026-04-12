@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if expected_type is not None:
        inferred_type = expected_type
    elif array is not None:
        if len(array) > 0:
            first_non_none = None
            for x in array:
                if x is not None:
                    first_non_none = x
                    break
            inferred_type = type(first_non_none) if first_non_none is not None else object
        else:
            inferred_type = object
    elif element is not None:
        inferred_type = type(element)
    else:
        inferred_type = object

    new_list = ArrayUtils._copy_list_grow1(array, inferred_type)
    new_list[len(new_list) - 1] = element
    return new_list