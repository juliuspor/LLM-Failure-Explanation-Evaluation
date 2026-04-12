@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is not None:
        inferred_type = None
        for x in array:
            if x is not None:
                inferred_type = type(x)
                break
    else:
        inferred_type = None
    if inferred_type is None and element is not None:
        inferred_type = type(element)
    if inferred_type is None and expected_type is not None:
        inferred_type = expected_type
    if inferred_type is None:
        inferred_type = object
    new_list = ArrayUtils._copy_list_grow1(array, inferred_type)
    new_list[len(new_list) - 1] = element
    if expected_type is not None:
        if inferred_type is not object and expected_type is not object and inferred_type is not expected_type:
            raise TypeError(
                f"Cannot cast object list to {expected_type.__name__} list "
                f"(ClassCastException: [Ljava.lang.Object; cannot be cast to "
                f"[Ljava.lang.{expected_type.__name__};)"
            )
    return new_list
