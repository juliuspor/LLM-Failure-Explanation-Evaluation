@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if expected_type is not None:
        inferred_type = expected_type
    else:
        inferred_type = None
        if array is not None and len(array) > 0:
            first_non_none = None
            for item in array:
                if item is not None:
                    first_non_none = item
                    break
            inferred_type = type(first_non_none) if first_non_none is not None else None
        if inferred_type is None:
            if element is not None:
                inferred_type = type(element)
            else:
                inferred_type = object
    new_list = ArrayUtils._copy_list_grow1(array, inferred_type)
    new_list[len(new_list) - 1] = element
    return new_list