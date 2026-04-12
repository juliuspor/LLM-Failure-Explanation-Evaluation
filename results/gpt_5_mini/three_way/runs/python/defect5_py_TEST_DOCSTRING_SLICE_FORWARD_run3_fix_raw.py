@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is not None:
        inferred_type = type(array)
    elif expected_type is not None:
        # If caller provided an expected_type, treat the resulting list as that component type
        inferred_type = expected_type
    elif element is not None:
        inferred_type = type(element)
    else:
        inferred_type = object

    new_list = ArrayUtils._copy_list_grow1(array, inferred_type)
    new_list[len(new_list) - 1] = element

    if expected_type is not None:
        # Simulate Java-style cast failure: if we couldn't determine a specific component
        # type (object) while expected_type is more specific, raise TypeError.
        if inferred_type == object and expected_type != object:
            raise TypeError(
                f"Cannot cast object list to {expected_type.__name__} list "
                f"(ClassCastException: [Ljava.lang.Object; cannot be cast to "
                f"[Ljava.lang.{expected_type.__name__};)"
            )
        # If we inferred a concrete type (from expected_type or element or array), and
        # element is not None, ensure element is an instance of expected_type.
        if element is not None and not isinstance(element, expected_type):
            raise TypeError(
                f"Cannot add element of type {type(element).__name__} to list of {expected_type.__name__}"
            )

    return new_list