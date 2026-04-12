@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if expected_type is not None:
        inferred_type = expected_type
    else:
        if array is not None:
            inferred_type = object
            for item in array:
                if item is not None:
                    inferred_type = type(item)
                    break
        elif element is not None:
            inferred_type = type(element)
        else:
            inferred_type = object

    new_list = ArrayUtils._copy_list_grow1(array, inferred_type)
    new_list[len(new_list) - 1] = element
    return new_list