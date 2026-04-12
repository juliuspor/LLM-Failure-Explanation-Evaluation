@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if expected_type is not None:
        component_type = expected_type
    else:
        component_type = None
    if array is not None:
        if component_type is None:
            for item in array:
                if item is not None:
                    component_type = type(item)
                    break
    if component_type is None and element is not None:
        component_type = type(element)
    if component_type is None:
        component_type = object
    if expected_type is not None and array is not None:
        for item in array:
            if item is not None:
                if type(item) is not expected_type:
                    raise TypeError(
                        f"Cannot cast {type(item).__name__} list to {expected_type.__name__} list "
                        f"(ClassCastException: [Ljava.lang.{type(item).__name__}; cannot be cast to "
                        f"[Ljava.lang.{expected_type.__name__};)"
                    )
                break
    new_list = ArrayUtils._copy_list_grow1(array, component_type)
    new_list[len(new_list) - 1] = element
    return new_list