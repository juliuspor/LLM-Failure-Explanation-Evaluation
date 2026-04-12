@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is not None:
        if len(array) > 0:
            inferred_element_type = type(array[0])
        else:
            inferred_element_type = None
    elif element is not None:
        inferred_element_type = type(element)
    else:
        inferred_element_type = None
    if expected_type is not None:
        element_type_to_use = expected_type
    else:
        element_type_to_use = inferred_element_type if inferred_element_type is not None else object
    new_list = ArrayUtils._copy_list_grow1(array, element_type_to_use)
    new_list[len(new_list) - 1] = element
    if expected_type is not None:
        if (inferred_element_type is None or inferred_element_type is object) and expected_type != object:
            if array is None and element is None:
                raise TypeError(
                    f"Cannot cast object list to {expected_type.__name__} list (ClassCastException: [Ljava.lang.Object; cannot be cast to [Ljava.lang.{expected_type.__name__};)"
                )
    return new_list