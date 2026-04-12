@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if expected_type is not None:
        inferred_type = expected_type
    elif array is not None:
        if len(array) > 0:
            inferred_type = object
            for item in array:
                if item is not None:
                    inferred_type = type(item)
                    break
            else:
                inferred_type = type(element) if element is not None else object
        else:
            inferred_type = type(element) if element is not None else object
    else:
        inferred_type = type(element) if element is not None else object
    if inferred_type == object and expected_type is not None:
        inferred_type = expected_type
    new_list = ArrayUtils._copy_list_grow1(array, inferred_type)
    new_list[len(new_list) - 1] = element
    return new_list