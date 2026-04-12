@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is not None:
        # Try to infer element type from existing array contents (first non-None element)
        inferred_element_type = None
        for item in array:
            if item is not None:
                inferred_element_type = type(item)
                break
        if inferred_element_type is None and expected_type is not None:
            inferred_element_type = expected_type
        if inferred_element_type is None:
            inferred_element_type = object
    elif element is not None:
        inferred_element_type = type(element)
    elif expected_type is not None:
        inferred_element_type = expected_type
    else:
        inferred_element_type = object

    new_list = ArrayUtils._copy_list_grow1(array, inferred_element_type)
    new_list[len(new_list) - 1] = element

    if expected_type is not None:
        # If we couldn't infer a concrete element type (object) but expected a concrete one, fail
        if inferred_element_type == object and expected_type != object:
            raise TypeError(
                f"Cannot cast object list to {expected_type.__name__} list "
                f"(ClassCastException: [Ljava.lang.Object; cannot be cast to "
                f"[Ljava.lang.{expected_type.__name__};)"
            )
        # If we inferred a concrete element type that doesn't match expected_type, fail as well
        if inferred_element_type is not object and inferred_element_type != expected_type:
            raise TypeError(
                f"Cannot cast {inferred_element_type.__name__} list to {expected_type.__name__} list "
                f"(ClassCastException: [Ljava.lang.{inferred_element_type.__name__}; cannot be cast to "
                f"[Ljava.lang.{expected_type.__name__};)"
            )

    return new_list