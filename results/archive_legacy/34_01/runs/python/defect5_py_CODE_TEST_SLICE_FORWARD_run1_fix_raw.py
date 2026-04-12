@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is not None:
        if len(array) > 0:
            inferred_type = type(array[0])
        else:
            inferred_type = None
    elif element is not None:
        inferred_type = type(element)
    elif expected_type is not None:
        inferred_type = expected_type
    else:
        inferred_type = object
    new_list = ArrayUtils._copy_list_grow1(array, inferred_type)
    new_list[len(new_list) - 1] = element
    if expected_type is not None and inferred_type is not None and inferred_type is not object and inferred_type is not expected_type:
        raise TypeError(
            f"Cannot cast object list to {expected_type.__name__} list "
            f"(ClassCastException: [Ljava.lang.Object; cannot be cast to "
            f"[Ljava.lang.{expected_type.__name__};)"
        )
    return new_list