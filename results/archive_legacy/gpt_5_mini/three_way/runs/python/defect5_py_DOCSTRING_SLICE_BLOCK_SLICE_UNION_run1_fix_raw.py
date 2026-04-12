@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is not None:
        inferred_element_type = None
        for item in array:
            if item is not None:
                inferred_element_type = type(item)
                break
    elif element is not None:
        inferred_element_type = type(element)
    else:
        inferred_element_type = None

    new_list = ArrayUtils._copy_list_grow1(array, inferred_element_type)
    new_list[len(new_list) - 1] = element

    if expected_type is not None and inferred_element_type is not None:
        try:
            if not issubclass(inferred_element_type, expected_type) and expected_type != object:
                raise TypeError(
                    f"Cannot cast object list to {expected_type.__name__} list "
                    f"(ClassCastException: [Ljava.lang.Object; cannot be cast to "
                    f"[Ljava.lang.{expected_type.__name__};)"
                )
        except TypeError:
            if inferred_element_type is not None and inferred_element_type is not object:
                raise
    return new_list