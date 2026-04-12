@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is not None:
        inferred_type = type(array)
    elif element is not None:
        inferred_type = type(element)
    elif expected_type is not None:
        # If both array and element are None but an expected_type is provided,
        # use expected_type as the inferred component type to avoid spurious cast errors.
        inferred_type = expected_type
    else:
        inferred_type = object

    new_list = ArrayUtils._copy_list_grow1(array, inferred_type)
    new_list[len(new_list) - 1] = element

    if expected_type is not None:
        # Only raise if we have a concrete inferred type that truly conflicts
        # with the expected_type. If inferred_type is object (unknown) accept it.
        if inferred_type is not object and inferred_type != expected_type:
            raise TypeError(
                f"Cannot cast object list to {expected_type.__name__} list "
                f"(ClassCastException: [Ljava.lang.Object; cannot be cast to "
                f"[Ljava.lang.{expected_type.__name__};)"
            )

    return new_list