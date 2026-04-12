@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is not None:
        # try to infer element type from first non-None element in array
        inferred_element_type = None
        for item in array:
            if item is not None:
                inferred_element_type = type(item)
                break
        if inferred_element_type is None:
            # array exists but all elements are None -> fall back to expected_type or object
            inferred_element_type = expected_type if expected_type is not None else object
    elif element is not None:
        inferred_element_type = type(element)
    else:
        # both array and element are None -> prefer expected_type if provided
        inferred_element_type = expected_type if expected_type is not None else object

    new_list = ArrayUtils._copy_list_grow1(array, inferred_element_type)
    new_list[len(new_list) - 1] = element

    if expected_type is not None:
        # If we have a concrete inferred type (not object), ensure it's compatible with expected_type
        if inferred_element_type is not object and not issubclass(inferred_element_type, expected_type):
            raise TypeError(
                f"Cannot cast {inferred_element_type.__name__} list to {expected_type.__name__} list "
                f"(ClassCastException: [Ljava.lang.{inferred_element_type.__name__}; cannot be cast to "
                f"[Ljava.lang.{expected_type.__name__};)"
            )
    return new_list