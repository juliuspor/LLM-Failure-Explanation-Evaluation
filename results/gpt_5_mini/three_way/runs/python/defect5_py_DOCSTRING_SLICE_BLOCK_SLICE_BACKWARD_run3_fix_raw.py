@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is not None:
        # Try to infer element type from array contents (first non-None element)
        inferred_type = None
        for item in array:
            if item is not None:
                inferred_type = type(item)
                break
        if inferred_type is None:
            # no concrete element found, fall back to list type
            inferred_type = type(array)
    elif element is not None:
        inferred_type = type(element)
    else:
        inferred_type = object

    new_list = ArrayUtils._copy_list_grow1(array, inferred_type)
    new_list[len(new_list) - 1] = element

    if expected_type is not None:
        # Only raise if we have a concrete inferred type that is incompatible
        if inferred_type is not object and not issubclass(inferred_type, expected_type):
            raise TypeError(
                f"Cannot cast {inferred_type.__name__} list to {expected_type.__name__} list "
                f"(ClassCastException: [Ljava.lang.{inferred_type.__name__}; cannot be cast to "
                f"[Ljava.lang.{expected_type.__name__};)"
            )
    return new_list