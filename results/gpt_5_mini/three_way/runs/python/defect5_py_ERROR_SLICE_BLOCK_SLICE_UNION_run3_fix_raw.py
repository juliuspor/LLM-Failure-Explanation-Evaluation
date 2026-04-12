@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is None:
        base_list: List[T] = []
    else:
        base_list = array.copy()

    # Determine runtime element type from existing elements if possible
    inferred_element_type: Optional[Type] = None
    if base_list:
        for item in base_list:
            if item is not None:
                inferred_element_type = type(item)
                break

    if inferred_element_type is None and element is not None:
        inferred_element_type = type(element)

    # If expected_type provided, validate existing elements and the new element
    if expected_type is not None and expected_type is not object:
        # Validate existing elements
        for i, item in enumerate(base_list):
            if item is not None and not isinstance(item, expected_type):
                raise TypeError(
                    f"Cannot cast list element at index {i} of type {type(item).__name__} to {expected_type.__name__}"
                )
        # Validate new element
        if element is not None and not isinstance(element, expected_type):
            raise TypeError(
                f"Cannot cast element of type {type(element).__name__} to {expected_type.__name__}"
            )

    # No expected_type or validation passed; append element
    base_list.append(element)
    return base_list