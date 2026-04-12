@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is not None:
        inferred_type = type(array)
        inferred_from = 'array'
    elif element is not None:
        inferred_type = type(element)
        inferred_from = 'element'
    else:
        inferred_type = None
        inferred_from = None

    new_list = ArrayUtils._copy_list_grow1(array, inferred_type)
    new_list[len(new_list) - 1] = element

    if expected_type is not None:
        # Only simulate a cast failure if the inferred type is exactly `object`
        # and that inference came from a real value (array or element). If both
        # were None, we cannot determine a component type and should not raise.
        if inferred_type is object and inferred_from is not None and expected_type != object:
            raise TypeError(
                f"Cannot cast object list to {expected_type.__name__} list "
                f"(ClassCastException: [Ljava.lang.Object; cannot be cast to "
                f"[Ljava.lang.{expected_type.__name__};)"
            )

    return new_list