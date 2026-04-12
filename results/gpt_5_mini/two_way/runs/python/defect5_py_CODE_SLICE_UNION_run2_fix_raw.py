@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is not None and len(array) > 0:
        # find first non-None element to infer element type
        inferred_element_type = None
        for item in array:
            if item is not None:
                inferred_element_type = type(item)
                break
        if inferred_element_type is None:
            # all elements are None, fall back to expected_type or object
            inferred_element_type = expected_type if expected_type is not None else object
    elif element is not None:
        inferred_element_type = type(element)
    else:
        inferred_element_type = expected_type if expected_type is not None else object

    new_list = ArrayUtils._copy_list_grow1(array, inferred_element_type)
    new_list[len(new_list) - 1] = element

    if expected_type is not None:
        # simulate Java-style ClassCastException when we only know 'object' element type
        if inferred_element_type is object and expected_type is not object:
            raise TypeError(
                f"Cannot cast object list to {expected_type.__name__} list "
                f"(ClassCastException: [Ljava.lang.Object; cannot be cast to "
                f"[Ljava.lang.{expected_type.__name__};)"
            )
    return new_list