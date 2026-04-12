@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is not None:
        # Try to infer the component type from the list's elements if possible
        inferred_component_type = object
        for item in array:
            if item is not None:
                inferred_component_type = type(item)
                break
        # If no non-None element found, fall back to object
    elif element is not None:
        inferred_component_type = type(element)
    elif expected_type is not None:
        # If both array and element are None but expected_type provided, use it
        inferred_component_type = expected_type
    else:
        inferred_component_type = object

    new_list = ArrayUtils._copy_list_grow1(array, inferred_component_type)
    new_list[len(new_list) - 1] = element

    if expected_type is not None:
        if inferred_component_type == object and expected_type != object:
            raise TypeError(
                f"Cannot cast object list to {expected_type.__name__} list "
                f"(ClassCastException: [Ljava.lang.Object; cannot be cast to "
                f"[Ljava.lang.{expected_type.__name__};)"
            )

    return new_list