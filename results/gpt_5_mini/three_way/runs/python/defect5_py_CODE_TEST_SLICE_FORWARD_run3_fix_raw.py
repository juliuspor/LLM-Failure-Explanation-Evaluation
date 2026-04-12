@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is not None:
        # try to infer element type from existing elements
        inferred_element_type = None
        for item in array:
            if item is not None:
                inferred_element_type = type(item)
                break
        if inferred_element_type is None:
            # fallback to expected_type or object
            inferred_element_type = expected_type if expected_type is not None else object
    elif element is not None:
        inferred_element_type = type(element)
    else:
        inferred_element_type = expected_type if expected_type is not None else object

    new_list = ArrayUtils._copy_list_grow1(array, inferred_element_type)
    # ensure new_list has at least one slot
    if len(new_list) == 0:
        new_list.append(element)
    else:
        new_list[-1] = element

    if expected_type is not None:
        # simulate Java-style cast failure: if inferred element type is object (unknown)
        # and expected_type is more specific, raise
        if inferred_element_type is object and expected_type is not object:
            raise TypeError(
                f"Cannot cast object list to {expected_type.__name__} list "
                f"(ClassCastException: [Ljava.lang.Object; cannot be cast to "
                f"[Ljava.lang.{expected_type.__name__};)"
            )
    return new_list