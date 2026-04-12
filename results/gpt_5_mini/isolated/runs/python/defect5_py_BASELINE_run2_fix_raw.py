@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is not None:
        # Try to infer element type from existing elements (first non-None)
        element_type = None
        for item in array:
            if item is not None:
                element_type = type(item)
                break
        if element_type is None:
            # array exists but all elements are None -> fallback to expected_type if given
            element_type = expected_type if expected_type is not None else object
    elif element is not None:
        element_type = type(element)
    elif expected_type is not None:
        element_type = expected_type
    else:
        element_type = object

    new_list = ArrayUtils._copy_list_grow1(array, element_type)
    new_list[len(new_list) - 1] = element

    if expected_type is not None:
        # Only raise if we have a concrete inferred element type incompatible with expected_type
        if element_type is not object and not issubclass(element_type, expected_type):
            raise TypeError(
                f"Cannot cast {element_type.__name__} list to {expected_type.__name__} list "
                f"(ClassCastException: [Ljava.lang.{element_type.__name__}; cannot be cast to "
                f"[Ljava.lang.{expected_type.__name__};)"
            )

    return new_list