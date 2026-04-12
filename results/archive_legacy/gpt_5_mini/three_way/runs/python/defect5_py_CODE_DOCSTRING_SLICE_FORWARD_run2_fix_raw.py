@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is not None:
        inferred_type = None
        for it in array:
            if it is not None:
                inferred_type = type(it)
                break
        if inferred_type is None:
            inferred_type = expected_type if expected_type is not None else object
    elif element is not None:
        inferred_type = type(element)
    else:
        inferred_type = object

    if element is not None and inferred_type is not object and not isinstance(element, inferred_type):
        raise TypeError(f"Element of type {type(element).__name__} is not compatible with inferred type {inferred_type.__name__}")

    new_list = ArrayUtils._copy_list_grow1(array, inferred_type)
    new_list[len(new_list) - 1] = element

    if expected_type is not None:
        if inferred_type is object and expected_type is not object:
            raise TypeError(
                f"Cannot cast object list to {expected_type.__name__} list "
                f"(ClassCastException: [Ljava.lang.Object; cannot be cast to "
                f"[Ljava.lang.{expected_type.__name__};)"
            )

    return new_list