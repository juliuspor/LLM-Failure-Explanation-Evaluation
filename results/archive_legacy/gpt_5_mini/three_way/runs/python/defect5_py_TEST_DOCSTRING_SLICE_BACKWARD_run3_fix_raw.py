@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is not None:
        if len(array) > 0:
            inferred_elem_type = type(array[0])
        else:
            inferred_elem_type = None
    elif element is not None:
        inferred_elem_type = type(element)
    else:
        inferred_elem_type = None

    new_list = ArrayUtils._copy_list_grow1(array, inferred_elem_type)
    new_list[len(new_list) - 1] = element

    if expected_type is not None:
        if inferred_elem_type is None:
            inferred_elem_type = expected_type
        else:
            if inferred_elem_type != object and expected_type != object and inferred_elem_type != expected_type:
                raise TypeError(
                    f"Cannot cast object list to {expected_type.__name__} list "
                    f"(ClassCastException: [Ljava.lang.Object; cannot be cast to "
                    f"[Ljava.lang.{expected_type.__name__};)"
                )
    return new_list