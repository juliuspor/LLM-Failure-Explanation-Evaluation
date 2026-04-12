@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is not None:
        inferred_type = object
        if len(array) > 0:
            for e in array:
                if e is not None:
                    inferred_type = type(e)
                    break
    elif element is not None:
        inferred_type = type(element)
    else:
        inferred_type = object

    if inferred_type == object and expected_type is not None:
        inferred_type = expected_type

    if expected_type is not None and inferred_type is not object and expected_type is not inferred_type:
        raise TypeError(
            f"Cannot cast object list to {expected_type.__name__} list "
            f"(ClassCastException: [Ljava.lang.Object; cannot be cast to "
            f"[Ljava.lang.{expected_type.__name__};)"
        )

    new_list = ArrayUtils._copy_list_grow1(array, inferred_type)
    new_list[len(new_list) - 1] = element
    return new_list