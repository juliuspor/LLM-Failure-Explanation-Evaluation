@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is not None:
        # Attempt to infer a component/element type from existing list contents
        component_type = object
        for item in array:
            if item is not None:
                component_type = type(item)
                break
    elif element is not None:
        component_type = type(element)
    else:
        component_type = object

    new_list = ArrayUtils._copy_list_grow1(array, component_type)
    new_list[len(new_list) - 1] = element

    if expected_type is not None:
        # Simulate Java array cast failure only in the ambiguous-case where
        # we have no concrete component type (object) but caller expects a
        # more specific type. If the array existed and had concrete element
        # types, do not raise here (Python lists are heterogeneous).
        if component_type is object and expected_type is not object:
            raise TypeError(
                f"Cannot cast object list to {expected_type.__name__} list "
                f"(ClassCastException: [Ljava.lang.Object; cannot be cast to "
                f"[Ljava.lang.{expected_type.__name__};)"
            )

    return new_list