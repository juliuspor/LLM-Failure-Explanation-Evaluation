@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if expected_type is not None:
        inferred_type = expected_type
    else:
        inferred_type = None
        # Try to infer from array contents (first non-None element)
        if array is not None:
            for item in array:
                if item is not None:
                    inferred_type = type(item)
                    break
        # If still unknown, infer from element
        if inferred_type is None and element is not None:
            inferred_type = type(element)
        # Default
        if inferred_type is None:
            inferred_type = object

    new_list = ArrayUtils._copy_list_grow1(array, inferred_type)
    new_list[len(new_list) - 1] = element

    # Simulate Java-like ClassCastException behavior: if we inferred a generic object
    # but an expected_type was specified and it's more specific, raise
    if expected_type is not None:
        # If inferred_type is object but expected_type is more specific, raise
        if inferred_type is object and expected_type != object:
            raise TypeError(
                f"Cannot cast object list to {expected_type.__name__} list "
                f"(ClassCastException: [Ljava.lang.Object; cannot be cast to "
                f"[Ljava.lang.{expected_type.__name__};)"
            )
    return new_list