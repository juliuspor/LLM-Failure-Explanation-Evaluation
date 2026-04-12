@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if expected_type is not None:
        inferred_type = expected_type
    elif element is not None:
        inferred_type = type(element)
    elif array is not None:
        inferred = object
        for x in array:
            if x is not None:
                inferred = type(x)
                break
        inferred_type = inferred
    else:
        inferred_type = object

    new_list = ArrayUtils._copy_list_grow1(array, inferred_type)
    new_list[len(new_list) - 1] = element

    return new_list