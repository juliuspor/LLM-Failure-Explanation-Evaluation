@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is not None and len(array) > 0:
        # infer element type from existing elements
        first_elem = array[0]
        inferred_element_type = type(first_elem) if first_elem is not None else None
    elif array is not None and len(array) == 0:
        # empty array: prefer expected_type if given, else unknown
        inferred_element_type = expected_type if expected_type is not None else None
    else:
        # array is None: prefer expected_type, else infer from element
        if expected_type is not None:
            inferred_element_type = expected_type
        elif element is not None:
            inferred_element_type = type(element)
        else:
            inferred_element_type = None

    new_list = ArrayUtils._copy_list_grow1(array, inferred_element_type)
    new_list[len(new_list) - 1] = element

    if expected_type is not None:
        # If we couldn't infer a specific element type (None) treat as generic/object
        # and raise if caller expects a more specific type to simulate cast failure
        if inferred_element_type is None and expected_type is not object:
            raise TypeError(
                f"Cannot cast object list to {expected_type.__name__} list "
                f"(ClassCastException: [Ljava.lang.Object; cannot be cast to "
                f"[Ljava.lang.{expected_type.__name__};)"
            )
    return new_list