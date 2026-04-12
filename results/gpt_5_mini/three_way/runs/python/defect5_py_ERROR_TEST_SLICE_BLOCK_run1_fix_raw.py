@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is not None:
        inferred_type = type(array)
    elif element is not None:
        inferred_type = type(element)
    else:
        inferred_type = object

    new_list = ArrayUtils._copy_list_grow1(array, inferred_type)
    new_list[len(new_list) - 1] = element

    if expected_type is not None:
        # If we couldn't infer a more specific type (object) but an expected_type
        # was provided, accept it and return the constructed list rather than
        # raising. This mirrors Java semantics more flexibly in Python.
        if inferred_type == object and expected_type != object:
            # No concrete component type to check against; treat as compatible.
            return new_list
        # Otherwise, if array had a concrete type that differs from expected_type,
        # simulate the original ClassCastException behavior by raising.
        if inferred_type != object and inferred_type != expected_type:
            raise TypeError(
                f"Cannot cast {inferred_type.__name__} list to {expected_type.__name__} list "
                f"(ClassCastException: [Ljava.lang.{inferred_type.__name__}; cannot be cast to "
                f"[Ljava.lang.{expected_type.__name__};)"
            )

    return new_list