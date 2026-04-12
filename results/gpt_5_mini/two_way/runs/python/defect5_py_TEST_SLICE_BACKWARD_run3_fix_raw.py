@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is not None:
        # Try to infer the element type from existing elements (first non-None)
        inferred_element_type = object
        for item in array:
            if item is not None:
                inferred_element_type = type(item)
                break
    elif element is not None:
        inferred_element_type = type(element)
    else:
        inferred_element_type = object

    new_list = ArrayUtils._copy_list_grow1(array, inferred_element_type)
    new_list[len(new_list) - 1] = element

    if expected_type is not None:
        # If we have a concrete inferred element type (not object) and it is incompatible
        # with expected_type, simulate a cast failure. If inferred is object, allow the
        # operation (None or unknown element types can fit into expected_type list).
        if inferred_element_type is not object and inferred_element_type is not expected_type:
            raise TypeError(
                f"Cannot cast {inferred_element_type.__name__} list to {expected_type.__name__} list "
                f"(ClassCastException: [Ljava.lang.{inferred_element_type.__name__}; cannot be cast to "
                f"[Ljava.lang.{expected_type.__name__};)"
            )

    return new_list