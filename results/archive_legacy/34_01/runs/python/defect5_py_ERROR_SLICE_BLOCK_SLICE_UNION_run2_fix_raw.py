@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is not None and len(array) > 0:
        inferred_type = None
        for it in array:
            if it is not None:
                inferred_type = type(it)
                break
        if inferred_type is None:
            if element is not None:
                inferred_type = type(element)
            else:
                inferred_type = object
    elif element is not None:
        inferred_type = type(element)
    else:
        inferred_type = object

    new_list = ArrayUtils._copy_list_grow1(array, inferred_type)
    new_list[len(new_list) - 1] = element

    if expected_type is not None and expected_type != object:
        for i, itm in enumerate(new_list):
            if itm is not None and not isinstance(itm, expected_type):
                raise TypeError(
                    f"Cannot cast object list to {expected_type.__name__} list "
                    f"(ClassCastException: [Ljava.lang.Object; cannot be cast to "
                    f"[Ljava.lang.{expected_type.__name__};)"
                )
    return new_list