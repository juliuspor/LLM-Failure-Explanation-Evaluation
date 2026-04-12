@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is None:
        # Start from empty list
        new_list = []
    else:
        new_list = array.copy()

    new_list.append(element)

    # Determine actual element type for simple runtime check:
    actual_type = None
    # Prefer explicit expected_type check: if array had elements, derive their type
    if len(new_list) > 0:
        # find first non-None element to infer type
        for item in new_list:
            if item is not None:
                actual_type = type(item)
                break
    # If no non-None items found, leave actual_type as None

    if expected_type is not None:
        # If we can determine an actual element type and it's not compatible with expected_type, raise
        if actual_type is not None and not issubclass(actual_type, expected_type):
            raise TypeError(
                f"Incompatible element type: cannot treat list of {actual_type.__name__} as list of {expected_type.__name__}"
            )
        # If actual_type is None (all elements None), we allow appending but if element itself is not None, check it
        if actual_type is None and element is not None and not issubclass(type(element), expected_type):
            raise TypeError(
                f"Incompatible element type: element of type {type(element).__name__} is not {expected_type.__name__}"
            )

    return new_list