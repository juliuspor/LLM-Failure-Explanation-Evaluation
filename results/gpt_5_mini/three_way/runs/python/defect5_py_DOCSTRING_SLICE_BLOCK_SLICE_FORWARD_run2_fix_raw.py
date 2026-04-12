@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is not None:
        inferred_type = type(array)
    elif element is not None:
        inferred_type = type(element)
    else:
        inferred_type = object

    new_list = ArrayUtils._copy_list_grow1(array, inferred_type)
    new_list[len(new_list) - 1] = element

    if expected_type is not None:
        # Only raise if we truly cannot treat the operation as compatible.
        # If the inferred type is a generic object list but the provided element
        # is an instance of the expected_type, allow the append. Otherwise,
        # simulate a Java ClassCastException when trying to cast an object[]
        # to a more specific component type.
        if inferred_type == object and expected_type != object:
            if not (element is None or isinstance(element, expected_type)):
                raise TypeError(
                    f"Cannot cast object list to {expected_type.__name__} list "
                    f"(ClassCastException: [Ljava.lang.Object; cannot be cast to "
                    f"[Ljava.lang.{expected_type.__name__};)"
                )

    return new_list