@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is not None and len(array) > 0:
        # try to find a concrete element type from existing elements
        inferred_elem_type = None
        for item in array:
            if item is not None:
                inferred_elem_type = type(item)
                break
        if inferred_elem_type is None:
            # no non-None elements, fall back to element's type or object
            inferred_elem_type = type(element) if element is not None else object
    else:
        # array is None or empty: infer from element or default to object
        inferred_elem_type = type(element) if element is not None else object

    new_list = ArrayUtils._copy_list_grow1(array, inferred_elem_type)
    # ensure the list is long enough and assign the last slot
    if len(new_list) == 0:
        new_list.append(element)
    else:
        new_list[len(new_list) - 1] = element

    if expected_type is not None:
        # Only raise if we truly have no information about element type (object)
        # and expected_type is more specific
        if inferred_elem_type is object and expected_type is not object:
            raise TypeError(
                f"Cannot cast object list to {expected_type.__name__} list "
                f"(ClassCastException: [Ljava.lang.Object; cannot be cast to "
                f"[Ljava.lang.{expected_type.__name__};)"
            )

    return new_list