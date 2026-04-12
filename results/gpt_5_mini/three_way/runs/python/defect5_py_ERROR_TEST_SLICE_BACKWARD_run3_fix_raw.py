@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is not None:
        # Try to infer component type from existing elements if possible
        inferred_type = object
        for item in array:
            if item is not None:
                inferred_type = type(item)
                break
        # If all elements None, fall back to expected_type if provided
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

    # If expected_type provided, simulate cast failure only when we truly have an
    # incompatible inferred component type (i.e., we inferred a specific type that
    # is not compatible with expected_type). If inferred_type is object (unknown),
    # allow creation since Python lists are heterogeneous.
    if expected_type is not None and inferred_type is not object:
        # Use issubclass checks when possible
        try:
            if not issubclass(inferred_type, expected_type):
                raise TypeError(
                    f"Cannot cast {inferred_type.__name__} list to {expected_type.__name__} list "
                    f"(ClassCastException: [Ljava.lang.{inferred_type.__name__}; cannot be cast to "
                    f"[Ljava.lang.{expected_type.__name__};)"
                )
        except TypeError:
            # If inferred_type is not a class/type that works with issubclass, don't raise
            pass

    return new_list