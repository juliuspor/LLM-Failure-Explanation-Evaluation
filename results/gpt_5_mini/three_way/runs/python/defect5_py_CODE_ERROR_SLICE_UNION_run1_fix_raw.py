@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is not None:
        # Try to infer the element type from the existing list's non-None elements
        inferred_elem_type = object
        for item in array:
            if item is not None:
                inferred_elem_type = type(item)
                break
    elif element is not None:
        inferred_elem_type = type(element)
    else:
        inferred_elem_type = object

    # If expected_type provided and we only know object as component type, simulate cast failure
    if expected_type is not None and inferred_elem_type is object and expected_type is not object:
        raise TypeError(
            f"Cannot cast object list to {expected_type.__name__} list "
            f"(ClassCastException: [Ljava.lang.Object; cannot be cast to "
            f"[Ljava.lang.{expected_type.__name__};)"
        )

    new_list = ArrayUtils._copy_list_grow1(array, inferred_elem_type)
    new_list[len(new_list) - 1] = element
    return new_list