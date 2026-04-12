@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is not None:
        element_type = None
        mixed = False
        for el in array:
            if el is not None:
                t = type(el)
                if element_type is None:
                    element_type = t
                elif element_type != t:
                    mixed = True
                    break
        if mixed:
            inferred_type = object
        else:
            inferred_type = element_type if element_type is not None else object
    elif element is not None:
        inferred_type = type(element)
    else:
        inferred_type = object

    new_list = ArrayUtils._copy_list_grow1(array, inferred_type)
    new_list[len(new_list) - 1] = element

    if expected_type is not None:
        if array is None:
            if inferred_type == object and expected_type != object:
                if element is None or not isinstance(element, expected_type):
                    raise TypeError(
                        f"Cannot cast object list to {expected_type.__name__} list "
                        f"(ClassCastException: [Ljava.lang.Object; cannot be cast to "
                        f"[Ljava.lang.{expected_type.__name__};)"
                    )
        else:
            for i, el in enumerate(new_list):
                if el is not None and not isinstance(el, expected_type):
                    raise TypeError(
                        f"Cannot cast object list to {expected_type.__name__} list "
                        f"(ClassCastException: [Ljava.lang.Object; cannot be cast to "
                        f"[Ljava.lang.{expected_type.__name__};)"
                    )
    return new_list