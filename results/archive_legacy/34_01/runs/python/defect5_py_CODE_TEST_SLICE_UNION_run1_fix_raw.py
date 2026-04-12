@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is not None:
        inferred_type = type(array)
    elif element is not None:
        inferred_type = type(element)
    else:
        inferred_type = expected_type if expected_type is not None else object

    new_list = ArrayUtils._copy_list_grow1(array, inferred_type)
    new_list[len(new_list) - 1] = element

    if array is not None and inferred_type == object and expected_type is not None and expected_type != object:
        raise TypeError(
            f"Cannot cast object list to {expected_type.__name__} list "
            f"(ClassCastException: [Ljava.lang.Object; cannot be cast to "
            f"[Ljava.lang.{expected_type.__name__};)"
        )

    return new_list