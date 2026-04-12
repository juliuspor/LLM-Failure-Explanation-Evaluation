@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is not None:
        # If array present, infer component type from array if possible
        # Find first non-None element to infer type
        inferred_component = None
        for item in array:
            if item is not None:
                inferred_component = type(item)
                break
        if inferred_component is None and expected_type is not None:
            inferred_component = expected_type
    elif expected_type is not None:
        inferred_component = expected_type
    elif element is not None:
        inferred_component = type(element)
    else:
        inferred_component = object

    # Create new list with one extra slot
    new_list = ArrayUtils._copy_list_grow1(array, inferred_component)
    new_list[len(new_list) - 1] = element

    # Enforce type checks only for non-None elements
    if expected_type is not None:
        # If expected_type provided, ensure any non-None element is instance of it
        if element is not None and not isinstance(element, expected_type):
            raise TypeError(
                f"Cannot cast element of type {type(element).__name__} to {expected_type.__name__}"
            )
        # Also ensure existing non-None elements in array match expected_type
        if array is not None:
            for i, item in enumerate(array):
                if item is not None and not isinstance(item, expected_type):
                    raise TypeError(
                        f"Cannot cast array element at index {i} of type {type(item).__name__} to {expected_type.__name__}"
                    )

    return new_list