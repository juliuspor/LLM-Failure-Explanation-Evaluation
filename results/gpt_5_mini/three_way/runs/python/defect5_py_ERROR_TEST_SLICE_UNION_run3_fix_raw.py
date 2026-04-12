@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if expected_type is not None and expected_type != object:
        inferred_type = expected_type
    else:
        # Try to infer from array contents if possible
        if array is not None and len(array) > 0:
            first_elem = array[0]
            inferred_type = type(first_elem) if first_elem is not None else object
        elif element is not None:
            inferred_type = type(element)
        else:
            inferred_type = object

    new_list = ArrayUtils._copy_list_grow1(array, inferred_type)
    new_list[len(new_list) - 1] = element

    # If expected_type was provided and is more specific than object, ensure compatibility
    if expected_type is not None and expected_type != object:
        # If inferred_type is object (unknown) it's acceptable to consider it compatible
        # If inferred_type is not a subclass of expected_type, raise TypeError to simulate cast failure
        try:
            # For builtin types, issubclass requires types, so guard
            if inferred_type is not object and not issubclass(inferred_type, expected_type):
                raise TypeError(
                    f"Cannot cast object list to {expected_type.__name__} list "
                    f"(ClassCastException: [Ljava.lang.Object; cannot be cast to "
                    f"[Ljava.lang.{expected_type.__name__};)"
                )
        except TypeError:
            # If issubclass check fails because inferred_type is not a class, skip strict checking
            pass

    return new_list