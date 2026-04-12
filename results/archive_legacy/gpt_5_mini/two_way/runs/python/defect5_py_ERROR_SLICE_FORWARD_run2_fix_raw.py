@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is not None:
        if len(array) > 0:
            first_non_none = None
            for itm in array:
                if itm is not None:
                    first_non_none = itm
                    break
            inferred_type = type(first_non_none) if first_non_none is not None else object
        else:
            inferred_type = object
    elif element is not None:
        inferred_type = type(element)
    else:
        inferred_type = object

    new_list = ArrayUtils._copy_list_grow1(array, inferred_type)
    new_list[len(new_list) - 1] = element

    if expected_type is not None:
        any_non_none = False
        for itm in new_list:
            if itm is not None:
                any_non_none = True
                if not isinstance(itm, expected_type):
                    raise TypeError(f"Cannot cast list element of type {type(itm).__name__} to {expected_type.__name__}")
        if not any_non_none and expected_type is not object:
            raise TypeError(f"Cannot cast object list to {expected_type.__name__} list (ClassCastException: [Ljava.lang.Object; cannot be cast to [Ljava.lang.{expected_type.__name__};)")

    return new_list