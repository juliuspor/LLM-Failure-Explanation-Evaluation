@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is not None:
        if len(array) > 0:
            first_non_none = None
            for itm in array:
                if itm is not None:
                    first_non_none = itm
                    break
            inferred_type = type(first_non_none) if first_non_none is not None else None
        else:
            inferred_type = None
    elif element is not None:
        inferred_type = type(element)
    else:
        inferred_type = None

    new_list = ArrayUtils._copy_list_grow1(array, inferred_type)
    new_list[len(new_list) - 1] = element

    if expected_type is not None:
        if inferred_type is not None and inferred_type != object and expected_type != object and inferred_type != expected_type:
            raise TypeError(
                f"Cannot cast object list to {expected_type.__name__} list "
                f"(ClassCastException: [Ljava.lang.Object; cannot be cast to "
                f"[Ljava.lang.{expected_type.__name__};)"
            )
    return new_list