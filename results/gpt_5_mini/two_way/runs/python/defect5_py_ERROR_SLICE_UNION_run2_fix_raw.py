@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is not None:
        # infer component type from array elements if possible
        inferred_type = type(array)
    elif expected_type is not None:
        # prefer expected_type when array is None to simulate typed array creation
        inferred_type = expected_type
    elif element is not None:
        inferred_type = type(element)
    else:
        inferred_type = object

    new_list = ArrayUtils._copy_list_grow1(array, inferred_type)
    new_list[len(new_list) - 1] = element

    if expected_type is not None:
        # If the inferred type is a generic object but expected_type is more specific,
        # allow it (simulating creating a typed array) by treating it as compatible.
        # Otherwise, if both are concrete and incompatible, raise TypeError.
        try:
            if inferred_type is not object and not issubclass(inferred_type, expected_type):
                raise TypeError(
                    f"Cannot cast {inferred_type.__name__} list to {expected_type.__name__} list "
                    f"(ClassCastException: [Ljava.lang.{inferred_type.__name__}; cannot be cast to "
                    f"[Ljava.lang.{expected_type.__name__};)"
                )
        except TypeError:
            # issubclass can raise a TypeError if expected_type is not a class; fall back to strict equality
            if inferred_type is not object and inferred_type != expected_type:
                raise TypeError(
                    f"Cannot cast {inferred_type.__name__} list to {expected_type.__name__} list "
                    f"(ClassCastException: [Ljava.lang.{inferred_type.__name__}; cannot be cast to "
                    f"[Ljava.lang.{expected_type.__name__};)"
                )

    return new_list