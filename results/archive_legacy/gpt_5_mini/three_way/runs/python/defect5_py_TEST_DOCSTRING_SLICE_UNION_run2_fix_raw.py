@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is not None:
        if len(array) == 0:
            inferred_type = None
        else:
            non_none_types = {type(x) for x in array if x is not None}
            if len(non_none_types) == 1:
                inferred_type = next(iter(non_none_types))
            elif len(non_none_types) == 0:
                inferred_type = None
            else:
                inferred_type = object
    elif element is not None:
        inferred_type = type(element)
    else:
        inferred_type = None

    if expected_type is not None:
        if inferred_type is None or inferred_type is object:
            inferred_type = expected_type
        elif inferred_type is not expected_type:
            raise TypeError(
                f"Cannot cast {inferred_type.__name__} list to {expected_type.__name__} list "
                f"(ClassCastException: [Ljava.lang.{inferred_type.__name__}; cannot be cast to "
                f"[Ljava.lang.{expected_type.__name__};)"
            )

    new_list = ArrayUtils._copy_list_grow1(array, inferred_type)
    new_list[len(new_list) - 1] = element
    return new_list