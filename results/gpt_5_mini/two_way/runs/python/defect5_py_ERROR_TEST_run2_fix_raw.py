@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if expected_type is not None:
        component_type = expected_type
    else:
        component_type = None

    # Try to infer component type from the existing array (look for first non-None element)
    if array is not None:
        for item in array:
            if item is not None:
                component_type = component_type or type(item)
                break

    # If still unknown, try from the element
    if component_type is None and element is not None:
        component_type = type(element)

    # Fallback to object
    if component_type is None:
        component_type = object

    # Create new list as a copy (functional style)
    new_list = ArrayUtils._copy_list_grow1(array, component_type)
    new_list[len(new_list) - 1] = element

    # Simulate Java ClassCastException behavior: if expected_type was provided and
    # we had to fall back to object (meaning no stronger type info) raise TypeError
    if expected_type is not None and component_type == object and expected_type != object:
        raise TypeError(
            f"Cannot cast object list to {expected_type.__name__} list (ClassCastException: [Ljava.lang.Object; cannot be cast to [Ljava.lang.{expected_type.__name__};)"
        )

    return new_list