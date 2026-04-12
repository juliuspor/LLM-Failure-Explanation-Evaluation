@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is not None and len(array) > 0:
        first_elem = array[0]
        if first_elem is None:
            # If first element is None, we cannot infer element type from array
            if element is not None:
                inferred_type = type(element)
            else:
                inferred_type = object
        else:
            inferred_type = type(first_elem)
    elif array is not None and len(array) == 0:
        # Empty array: infer from element if available
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

    if expected_type is not None:
        if inferred_type == object and expected_type != object:
            raise TypeError(
                f"Cannot cast object list to {expected_type.__name__} list "
                f"(ClassCastException: [Ljava.lang.Object; cannot be cast to "
                f"[Ljava.lang.{expected_type.__name__};)"
            )

    return new_list