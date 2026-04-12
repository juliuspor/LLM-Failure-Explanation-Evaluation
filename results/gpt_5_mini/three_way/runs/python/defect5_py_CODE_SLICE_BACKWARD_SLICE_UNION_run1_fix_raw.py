@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is not None:
        # infer element type from first non-None element in the list
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

    if expected_type is not None:
        # If we couldn't infer element type (both array elements and element are None),
        # and expected_type is not the generic object, simulate a cast failure.
        if inferred_element_type is None and expected_type is not object:
            raise TypeError(
                f"Cannot cast object list to {expected_type.__name__} list "
                f"(ClassCastException: [Ljava.lang.Object; cannot be cast to "
                f"[Ljava.lang.{expected_type.__name__};)"
            )
        # If we inferred a specific type, ensure it's compatible with expected_type
        if inferred_element_type is not None and not issubclass(inferred_element_type, expected_type):
            raise TypeError(
                f"Cannot cast {inferred_element_type.__name__} list to {expected_type.__name__} list "
                f"(ClassCastException: [Ljava.lang.{inferred_element_type.__name__}; cannot be cast to "
                f"[Ljava.lang.{expected_type.__name__};)"
            )

    return new_list