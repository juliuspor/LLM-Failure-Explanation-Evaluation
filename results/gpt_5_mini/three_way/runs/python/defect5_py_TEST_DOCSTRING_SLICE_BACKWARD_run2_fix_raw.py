@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is not None:
        # Determine component type from array contents: first non-None element
        inferred_component_type = None
        for item in array:
            if item is not None:
                inferred_component_type = type(item)
                break
        # If all elements are None, but expected_type provided, use it
        if inferred_component_type is None and expected_type is not None:
            inferred_component_type = expected_type
    elif element is not None:
        inferred_component_type = type(element)
    else:
        # both array and element are None
        inferred_component_type = expected_type if expected_type is not None else object

    new_list = ArrayUtils._copy_list_grow1(array, inferred_component_type)
    new_list[len(new_list) - 1] = element

    # If expected_type provided, simulate Java-style cast check: if we know
    # the inferred component type and it's not compatible with expected_type,
    # raise TypeError. If inferred is object (unknown) but expected_type is
    # provided, allow (we can create list of expected type containing None).
    if expected_type is not None:
        # If inferred_component_type is object or matches expected_type or is subclass, allow
        if inferred_component_type is object:
            # unknown component type; allow creation for expected_type
            pass
        else:
            # If inferred component type is not subclass of expected_type, raise
            try:
                is_compatible = issubclass(inferred_component_type, expected_type)
            except TypeError:
                # If inferred_component_type is not a class, compare types directly
                is_compatible = inferred_component_type == expected_type
            if not is_compatible:
                raise TypeError(
                    f"Cannot cast object list to {expected_type.__name__} list "
                    f"(ClassCastException: [Ljava.lang.Object; cannot be cast to "
                    f"[Ljava.lang.{expected_type.__name__};)"
                )

    return new_list