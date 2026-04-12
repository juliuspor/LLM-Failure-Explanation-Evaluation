@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is not None and len(array) > 0:
        # Find first non-None element to infer element type
        inferred_elem_type = object
        for item in array:
            if item is not None:
                inferred_elem_type = type(item)
                break
    elif array is not None:
        # array exists but empty
        inferred_elem_type = object
    elif element is not None:
        inferred_elem_type = type(element)
    else:
        inferred_elem_type = object

    new_list = ArrayUtils._copy_list_grow1(array, inferred_elem_type)
    # Ensure list has at least one slot to assign
    if len(new_list) == 0:
        new_list.append(element)
    else:
        new_list[len(new_list) - 1] = element

    if expected_type is not None:
        if inferred_elem_type == object and expected_type != object:
            raise TypeError(
                f"Cannot cast object list to {expected_type.__name__} list "
                f"(ClassCastException: [Ljava.lang.Object; cannot be cast to "
                f"[Ljava.lang.{expected_type.__name__};)"
            )
    return new_list