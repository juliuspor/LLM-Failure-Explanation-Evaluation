@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is not None:
        inferred_type = object
        for el in array:
            if el is not None:
                inferred_type = type(el)
                break
    else:
        inferred_type = None
    if element is not None:
        element_type = type(element)
        if inferred_type is None or inferred_type == object:
            inferred_type = element_type
        elif inferred_type != element_type:
            if expected_type is None:
                inferred_type = element_type
            else:
                if inferred_type != expected_type and element_type != expected_type:
                    raise TypeError(f"Cannot add element of type {element_type.__name__} to list of type {inferred_type.__name__}")
                inferred_type = expected_type
    if inferred_type is None or inferred_type == object:
        if expected_type is not None:
            inferred_type = expected_type
        else:
            inferred_type = object
    new_list = ArrayUtils._copy_list_grow1(array, inferred_type)
    new_list[len(new_list) - 1] = element
    return new_list