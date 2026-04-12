@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is not None:
        # Try to infer component type from existing elements (first non-None element)
        inferred_type = object
        for item in array:
            if item is not None:
                inferred_type = type(item)
                break
        # If no non-None elements, prefer expected_type if provided
        if inferred_type is object and expected_type is not None:
            inferred_type = expected_type
    elif element is not None:
        inferred_type = type(element)
    elif expected_type is not None:
        inferred_type = expected_type
    else:
        inferred_type = object

    new_list = ArrayUtils._copy_list_grow1(array, inferred_type)
    new_list[len(new_list) - 1] = element

    if expected_type is not None:
        # If we have a concrete inferred type (not object) and it conflicts with expected_type, raise
        if inferred_type is not object and expected_type is not object and inferred_type != expected_type:
            raise TypeError(
                f"Cannot cast {inferred_type.__name__} list to {expected_type.__name__} list "
                f"(ClassCastException: [Ljava.lang.{inferred_type.__name__}; cannot be cast to "
                f"[Ljava.lang.{expected_type.__name__};)"
            )

    return new_list