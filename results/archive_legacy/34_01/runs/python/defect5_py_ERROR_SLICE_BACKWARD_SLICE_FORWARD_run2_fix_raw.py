@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is not None:
        inferred_element_type = None
        for e in array:
            if e is not None:
                inferred_element_type = type(e)
                break
        if inferred_element_type is None:
            inferred_element_type = type(element) if element is not None else object
    elif element is not None:
        inferred_element_type = type(element)
    else:
        inferred_element_type = object

    if expected_type is not None and inferred_element_type is not object:
        if not issubclass(inferred_element_type, expected_type) and not issubclass(expected_type, inferred_element_type):
            raise TypeError(
                f"Cannot cast {inferred_element_type.__name__} list to {expected_type.__name__} list "
                f"(ClassCastException: [{inferred_element_type.__name__}] cannot be cast to [{expected_type.__name__}])"
            )

    new_list = ArrayUtils._copy_list_grow1(array, inferred_element_type)
    new_list[len(new_list) - 1] = element
    return new_list