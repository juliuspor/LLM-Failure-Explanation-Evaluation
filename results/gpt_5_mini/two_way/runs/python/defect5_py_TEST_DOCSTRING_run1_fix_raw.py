@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if expected_type is not None:
        inferred_type = expected_type
    else:
        if array is not None:
            inferred_type = type(array)
        elif element is not None:
            inferred_type = type(element)
        else:
            inferred_type = object

    if array is None:
        # Create a new list containing the single element
        new_list: List[T] = [element]
    else:
        new_list = ArrayUtils._copy_list_grow1(array, inferred_type)
        new_list[len(new_list) - 1] = element

    if expected_type is not None:
        # Simulate Java-style ClassCastException when attempting to cast an Object[] to a more specific type
        # If inferred_type was object (unknown) but expected_type is more specific, allow creation (None can be in any array)
        # However, if inferred_type is not object and does not match expected_type, raise
        if inferred_type != object and inferred_type != expected_type:
            raise TypeError(
                f"Cannot cast object list to {expected_type.__name__} list "
                f"(ClassCastException: [Ljava.lang.Object; cannot be cast to "
                f"[Ljava.lang.{expected_type.__name__};)"
            )
    return new_list