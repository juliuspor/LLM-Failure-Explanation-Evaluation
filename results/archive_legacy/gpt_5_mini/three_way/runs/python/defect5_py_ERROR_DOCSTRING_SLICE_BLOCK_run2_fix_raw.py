@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is not None:
        # determine component type from array: first non-None element
        component_type = None
        for item in array:
            if item is not None:
                component_type = type(item)
                break
        if component_type is None:
            component_type = object
    elif element is not None:
        component_type = type(element)
    elif expected_type is not None:
        component_type = expected_type
    else:
        component_type = object

    new_list = ArrayUtils._copy_list_grow1(array, component_type)
    new_list[len(new_list) - 1] = element

    if expected_type is not None:
        if component_type is not object and expected_type is not object and component_type != expected_type:
            raise TypeError(
                f"Cannot cast {component_type.__name__} list to {expected_type.__name__} list "
                f"(ClassCastException: [Ljava.lang.{component_type.__name__}; cannot be cast to "
                f"[Ljava.lang.{expected_type.__name__};)"
            )
    return new_list