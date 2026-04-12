@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is not None:
        inferred_type = None
        for e in array:
            if e is not None:
                inferred_type = type(e)
                break
        if inferred_type is None:
            inferred_type = expected_type if expected_type is not None else object
    elif element is not None:
        inferred_type = type(element)
    else:
        inferred_type = expected_type if expected_type is not None else object

    if inferred_type is object and expected_type is not None:
        inferred_type = expected_type

    if expected_type is not None and inferred_type is not object and inferred_type != expected_type:
        raise TypeError(
            f"Cannot cast {inferred_type.__name__} list to {expected_type.__name__} list "
            f"(ClassCastException: [Ljava.lang.{inferred_type.__name__}; cannot be cast to "
            f"[Ljava.lang.{expected_type.__name__};)"
        )

    new_list = ArrayUtils._copy_list_grow1(array, inferred_type)
    new_list[len(new_list) - 1] = element
    return new_list