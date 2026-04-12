@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is not None:
        inferred_type = type(array)
    elif element is not None:
        inferred_type = type(element)
    else:
        inferred_type = object

    # If expected_type is provided, enforce it:
    # - If we have no concrete type info (inferred_type is object) and expected_type is not object,
    #   simulate Java ClassCastException by raising TypeError.
    # - If element is not None, ensure it's an instance of expected_type.
    if expected_type is not None:
        if inferred_type == object and expected_type != object:
            raise TypeError(
                f"Cannot cast object list to {expected_type.__name__} list "
                f"(ClassCastException: [Ljava.lang.Object; cannot be cast to "
                f"[Ljava.lang.{expected_type.__name__};)"
            )
        if element is not None and not isinstance(element, expected_type):
            raise TypeError(
                f"Element of type {type(element).__name__} cannot be added to list of {expected_type.__name__}"
            )

    new_list = ArrayUtils._copy_list_grow1(array, inferred_type)
    new_list[len(new_list) - 1] = element

    return new_list