@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is not None:
        # Determine if array has any concrete non-None elements to infer type
        concrete_type = None
        for itm in array:
            if itm is not None:
                concrete_type = type(itm)
                break
        inferred_type = concrete_type if concrete_type is not None else (expected_type if expected_type is not None else type(array))
    elif element is not None:
        inferred_type = type(element)
    else:
        inferred_type = expected_type if expected_type is not None else object

    new_list = ArrayUtils._copy_list_grow1(array, inferred_type)
    new_list[len(new_list) - 1] = element

    if expected_type is not None:
        # If we have a concrete inferred_type (not object), ensure compatibility with expected_type
        if inferred_type is not object and inferred_type is not None and not issubclass(inferred_type, expected_type):
            raise TypeError(
                f"Cannot cast {inferred_type.__name__} list to {expected_type.__name__} list "
                f"(ClassCastException: [Ljava.lang.{inferred_type.__name__}; cannot be cast to "
                f"[Ljava.lang.{expected_type.__name__};)"
            )

    return new_list