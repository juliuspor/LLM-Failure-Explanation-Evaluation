@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is not None:
        inferred_type = type(array)
    elif expected_type is not None:
        inferred_type = expected_type
    elif element is not None:
        inferred_type = type(element)
    else:
        inferred_type = object
    
    new_list = ArrayUtils._copy_list_grow1(array, inferred_type)
    new_list[len(new_list) - 1] = element
    
    return new_list

    # Type check moved after assignment to allow None elements
    if expected_type is not None and array is None and inferred_type == object:
        if expected_type != object:
            raise TypeError(
                f"Cannot cast object list to {expected_type.__name__} list "
                f"(ClassCastException: [Ljava.lang.Object; cannot be cast to "
                f"[Ljava.lang.{expected_type.__name__};)"
            )