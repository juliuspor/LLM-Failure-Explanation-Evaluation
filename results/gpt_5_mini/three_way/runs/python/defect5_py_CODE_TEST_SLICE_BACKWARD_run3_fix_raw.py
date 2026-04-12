@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is not None:
        # infer component type from first non-None element if possible
        inferred_type = object
        for item in array:
            if item is not None:
                inferred_type = type(item)
                break
        # if all elements are None, try expected_type
        if inferred_type is object and expected_type is not None:
            inferred_type = expected_type
    elif element is not None:
        inferred_type = type(element)
    else:
        # both array and element are None
        inferred_type = expected_type if expected_type is not None else object

    # If expected_type is provided, validate compatibility
    if expected_type is not None:
        # If inferred_type is object, adopt expected_type for construction
        if inferred_type is object:
            inferred_type = expected_type
        else:
            # Check that inferred_type is subclass of expected_type or same
            try:
                if not issubclass(inferred_type, expected_type):
                    raise TypeError(
                        f"Cannot cast {inferred_type.__name__} list to {expected_type.__name__} list "
                        f"(ClassCastException: [Ljava.lang.{inferred_type.__name__}; cannot be cast to "
                        f"[Ljava.lang.{expected_type.__name__};)"
                    )
            except TypeError:
                # issubclass can raise TypeError if inferred_type is not a class
                # fall back to equality check
                if inferred_type != expected_type:
                    raise TypeError(
                        f"Cannot cast {inferred_type} list to {expected_type.__name__} list "
                        f"(ClassCastException)"
                    )

    new_list = ArrayUtils._copy_list_grow1(array, inferred_type)
    new_list[len(new_list) - 1] = element
    return new_list