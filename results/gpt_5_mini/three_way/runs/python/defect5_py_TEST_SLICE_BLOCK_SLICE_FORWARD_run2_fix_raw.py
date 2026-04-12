@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is not None:
        # If array exists, infer element type from its elements if possible
        inferred_type = type(array)
    elif element is not None:
        inferred_type = type(element)
    else:
        inferred_type = object

    # If expected_type is provided and we only inferred object (unknown),
    # adopt expected_type as the component type instead of raising.
    if expected_type is not None and inferred_type == object and expected_type != object:
        inferred_type = expected_type

    new_list = ArrayUtils._copy_list_grow1(array, inferred_type)
    new_list[len(new_list) - 1] = element

    if expected_type is not None:
        # Only raise if we have a concrete mismatch between inferred_type and expected_type
        # For example, an array of a concrete type that is not compatible with expected_type.
        if inferred_type != expected_type and inferred_type is not object:
            raise TypeError(
                f"Cannot cast {inferred_type.__name__} list to {expected_type.__name__} list "
                f"(ClassCastException: [Ljava.lang.{inferred_type.__name__}; cannot be cast to "
                f"[Ljava.lang.{expected_type.__name__};)"
            )

    return new_list