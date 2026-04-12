@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is not None:
        if len(array) > 0:
            inferred_elem_type = type(array[0])
        else:
            inferred_elem_type = None
    elif element is not None:
        inferred_elem_type = type(element)
    else:
        inferred_elem_type = None

    if inferred_elem_type is None:
        if expected_type is not None:
            inferred_elem_type = expected_type
        else:
            inferred_elem_type = object

    if expected_type is not None and inferred_elem_type is not object:
        if not (inferred_elem_type == expected_type or issubclass(inferred_elem_type, expected_type)):
            raise TypeError(
                f"Cannot cast {inferred_elem_type.__name__} list to {expected_type.__name__} list (ClassCastException)"
            )

    new_list = ArrayUtils._copy_list_grow1(array, inferred_elem_type)
    new_list[len(new_list) - 1] = element
    return new_list