@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is not None:
        # try to infer component type from first non-None element
        inferred_type = None
        for item in array:
            if item is not None:
                inferred_type = type(item)
                break
        if inferred_type is None:
            # no non-None elements, fall back to object to indicate unknown
            inferred_type = object
    elif element is not None:
        inferred_type = type(element)
    else:
        inferred_type = object

    new_list = ArrayUtils._copy_list_grow1(array, inferred_type)
    new_list[len(new_list) - 1] = element

    if expected_type is not None:
        # Only raise if we truly don't know the component type (object) and expected_type is more specific
        if inferred_type == object and expected_type != object:
            raise TypeError(
                f"Cannot cast object list to {expected_type.__name__} list "
                f"(ClassCastException: [Ljava.lang.Object; cannot be cast to "
                f"[Ljava.lang.{expected_type.__name__};)"
            )
        # Additionally, if we inferred a concrete type and the element doesn't match expected_type, raise
        if inferred_type is not object and element is not None and not isinstance(element, expected_type):
            raise TypeError(
                f"Element of type {type(element).__name__} cannot be added to list of {expected_type.__name__}"
            )

    return new_list