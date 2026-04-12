@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is not None:
        # Try to infer component type from existing elements (first non-None)
        component_type = None
        for item in array:
            if item is not None:
                component_type = type(item)
                break
        if component_type is None:
            # No non-None elements: prefer expected_type if given, else object
            component_type = expected_type if expected_type is not None else object
    elif element is not None:
        component_type = type(element)
    else:
        # Both array and element are None: use expected_type if provided else object
        component_type = expected_type if expected_type is not None else object

    new_list = ArrayUtils._copy_list_grow1(array, component_type)
    new_list[len(new_list) - 1] = element

    if expected_type is not None:
        # Simulate a class cast failure when we only know component as object but expected is more specific
        if component_type is object and expected_type != object:
            raise TypeError(
                f"Cannot cast object list to {expected_type.__name__} list "
                f"(ClassCastException: [Ljava.lang.Object; cannot be cast to "
                f"[Ljava.lang.{expected_type.__name__};)"
            )

    return new_list