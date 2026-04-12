@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is None:
        inferred_type = type(element) if element is not None else object
    else:
        inferred_type = object
        for x in array:
            if x is not None:
                inferred_type = type(x)
                break
        if inferred_type is object and element is not None:
            inferred_type = type(element)
    new_list = ArrayUtils._copy_list_grow1(array, inferred_type)
    new_list[len(new_list) - 1] = element
    if expected_type is not None:
        if array is None:
            non_none_elements = [element] if element is not None else []
        else:
            non_none_elements = [x for x in array if x is not None]
            if element is not None:
                non_none_elements.append(element)
        for e in non_none_elements:
            if not isinstance(e, expected_type):
                raise TypeError(
                    f"Cannot cast list with element type {type(e).__name__} to {expected_type.__name__} list "
                    f"(ClassCastException: [Ljava.lang.Object; cannot be cast to [Ljava.lang.{expected_type.__name__};)"
                )
    return new_list