@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if expected_type is not None:
        # use expected_type as the component (element) type
        component_type = expected_type
    else:
        component_type = None

    # infer element type from array contents or the element itself
    if array is not None and len(array) > 0:
        # try to infer from first non-None element
        first_type = None
        for item in array:
            if item is not None:
                first_type = type(item)
                break
        inferred_element_type = first_type if first_type is not None else (type(element) if element is not None else None)
    else:
        inferred_element_type = type(element) if element is not None else None

    # If expected_type given and we have an inferred concrete element type that is incompatible, raise
    if expected_type is not None and inferred_element_type is not None:
        if not issubclass(inferred_element_type, expected_type):
            raise TypeError(
                f"Cannot cast list element type {inferred_element_type.__name__} to {expected_type.__name__}"
            )

    # create new list extended by one slot
    new_list = ArrayUtils._copy_list_grow1(array, expected_type or inferred_element_type)
    new_list[len(new_list) - 1] = element

    return new_list