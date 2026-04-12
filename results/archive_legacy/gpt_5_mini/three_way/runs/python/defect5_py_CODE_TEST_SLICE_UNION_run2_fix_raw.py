@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is not None:
        inferred_element_type = None
        for el in array:
            if el is not None:
                inferred_element_type = type(el)
                break
        if inferred_element_type is None:
            inferred_element_type = expected_type if expected_type is not None else object
    elif element is not None:
        inferred_element_type = type(element)
    else:
        inferred_element_type = expected_type if expected_type is not None else object

    if inferred_element_type == object and expected_type is not None:
        inferred_element_type = expected_type

    new_list = ArrayUtils._copy_list_grow1(array, inferred_element_type)
    new_list[len(new_list) - 1] = element

    if expected_type is not None:
        if inferred_element_type is not object and inferred_element_type != expected_type:
            raise TypeError(
                f"Cannot cast {inferred_element_type.__name__} list to {expected_type.__name__} list"
            )
    return new_list