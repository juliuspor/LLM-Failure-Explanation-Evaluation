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
        # Only raise if we have a concrete inferred type that's incompatible
        try:
            inferred_is_object = (inferred_type is object)
        except Exception:
            inferred_is_object = False
        if not inferred_is_object and expected_type is not object:
            # If inferred_type isn't a subclass of expected_type, it's incompatible
            # Use issubclass only for class types
            if isinstance(inferred_type, type) and not issubclass(inferred_type, expected_type):
                raise TypeError(
                    f"Cannot cast {inferred_type.__name__} list to {expected_type.__name__} list "
                    f"(ClassCastException: [Ljava.lang.{inferred_type.__name__}; cannot be cast to "
                    f"[Ljava.lang.{expected_type.__name__};)"
                )

    return new_list