@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is not None:
        # find actual component type from existing elements (first non-None)
        component_type = None
        for e in array:
            if e is not None:
                component_type = type(e)
                break
        if component_type is None:
            # array exists but all elements are None -> fall back to object
            component_type = object
    elif element is not None:
        component_type = type(element)
    else:
        component_type = object

    new_list = ArrayUtils._copy_list_grow1(array, component_type)
    new_list[len(new_list) - 1] = element

    if expected_type is not None:
        if component_type == object and expected_type != object:
            raise TypeError(
                f"Cannot cast object list to {expected_type.__name__} list "
                f"(ClassCastException: [Ljava.lang.Object; cannot be cast to "
                f"[Ljava.lang.{expected_type.__name__};)"
            )

    return new_list