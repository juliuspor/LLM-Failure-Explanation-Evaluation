@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is not None and len(array) > 0:
        # infer from first non-None element in array
        inferred_component_type = None
        for item in array:
            if item is not None:
                inferred_component_type = type(item)
                break
        if inferred_component_type is None:
            # all elements are None - fall back to element or expected_type
            inferred_component_type = type(element) if element is not None else (expected_type if expected_type is not None else object)
    else:
        inferred_component_type = type(element) if element is not None else (expected_type if expected_type is not None else object)

    new_list = ArrayUtils._copy_list_grow1(array, inferred_component_type)
    new_list[len(new_list) - 1] = element

    if expected_type is not None and expected_type is not object:
        # If we can determine a concrete component type and it's incompatible, raise
        if inferred_component_type is not object and not issubclass(inferred_component_type, expected_type):
            raise TypeError(
                f"Cannot cast element type {inferred_component_type.__name__} to {expected_type.__name__} (ClassCastException)"
            )
    return new_list