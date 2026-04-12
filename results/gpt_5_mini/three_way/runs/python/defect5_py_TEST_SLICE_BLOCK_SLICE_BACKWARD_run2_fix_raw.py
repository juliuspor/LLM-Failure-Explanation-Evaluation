@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is not None:
        inferred_type = type(array)
    elif element is not None:
        inferred_type = type(element)
    elif expected_type is not None:
        inferred_type = expected_type
    else:
        inferred_type = object

    new_list = ArrayUtils._copy_list_grow1(array, inferred_type)
    new_list[len(new_list) - 1] = element

    if expected_type is not None:
        if inferred_type == object and expected_type != object:
            # If we couldn't infer a more specific type (object) and expected_type is
            # more specific, allow the operation when both inputs were None by
            # treating the new list as compatible. Only raise when array was present
            # and its type conflicts with expected_type.
            if array is not None:
                raise TypeError(
                    f"Cannot cast object list to {expected_type.__name__} list "
                    f"(ClassCastException: [Ljava.lang.Object; cannot be cast to "
                    f"[Ljava.lang.{expected_type.__name__};)"
                )
        else:
            # If we have an inferred type from element or expected_type, check compatibility
            if inferred_type is not object and expected_type is not object and inferred_type != expected_type:
                # mismatch between inferred and expected
                raise TypeError(
                    f"Cannot cast {inferred_type.__name__} list to {expected_type.__name__} list"
                )

    return new_list