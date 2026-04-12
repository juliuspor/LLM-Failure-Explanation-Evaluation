@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is not None:
        inferred_type = type(array)
    elif element is not None:
        inferred_type = type(element)
    else:
        inferred_type = object
    saw_non_none = False
    if array is not None:
        for item in array:
            if item is not None:
                saw_non_none = True
                inferred_type = type(item)
                break
    elif element is not None:
        saw_non_none = True
    new_list = ArrayUtils._copy_list_grow1(array, inferred_type)
    new_list[len(new_list) - 1] = element
    if expected_type is not None:
        if inferred_type == object and expected_type != object and saw_non_none:
            raise TypeError(
                f"Cannot cast object list to {expected_type.__name__} list "
                f"(ClassCastException: [Ljava.lang.Object; cannot be cast to "
                f"[Ljava.lang.{expected_type.__name__};)"
            )
    return new_list
