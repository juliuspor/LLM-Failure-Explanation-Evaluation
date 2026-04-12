@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is not None:
        saw_non_none = False
        elem_type = None
        for it in array:
            if it is not None:
                saw_non_none = True
                elem_type = type(it)
                break
        if saw_non_none:
            inferred_type = elem_type
        else:
            inferred_type = object
    elif element is not None:
        inferred_type = type(element)
    else:
        inferred_type = object
    new_list = ArrayUtils._copy_list_grow1(array, inferred_type)
    new_list[len(new_list) - 1] = element
    if expected_type is not None:
        if inferred_type == object and expected_type != object:
            inferred_type = expected_type
        elif inferred_type != object and expected_type != object and inferred_type != expected_type:
            raise TypeError(
                f"Cannot cast {inferred_type.__name__} list to {expected_type.__name__} list "
                f"(ClassCastException: [Ljava.lang.{inferred_type.__name__}; cannot be cast to "
                f"[Ljava.lang.{expected_type.__name__};)"
            )
    return new_list