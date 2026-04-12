@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is not None:
        # Try infer element type from array: use type of first non-None element if possible
        inferred_type = None
        for item in array:
            if item is not None:
                inferred_type = type(item)
                break
        # If array had no non-None elements, and element provided, use its type
        if inferred_type is None and element is not None:
            inferred_type = type(element)
        # If still None, leave as None (unknown)
    elif element is not None:
        inferred_type = type(element)
    else:
        inferred_type = None

    new_list = ArrayUtils._copy_list_grow1(array, inferred_type)
    new_list[len(new_list) - 1] = element

    if expected_type is not None:
        # Only raise if we have evidence that the inferred type conflicts with expected_type
        if inferred_type is not None and inferred_type is not object and inferred_type != expected_type:
            raise TypeError(
                f"Cannot cast {inferred_type.__name__} list to {expected_type.__name__} list "
                f"(ClassCastException: [Ljava.lang.{inferred_type.__name__}; cannot be cast to "
                f"[Ljava.lang.{expected_type.__name__};)"
            )
    return new_list