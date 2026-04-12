@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is not None:
        inferred_type = type(array)
    elif element is not None:
        inferred_type = type(element)
    else:
        inferred_type = object

    # If array is None or empty and an expected_type is provided, prefer expected_type
    if expected_type is not None:
        if array is None or len(array) == 0:
            inferred_component = expected_type
        else:
            # infer component type from existing elements if possible
            # try to find a non-None element to determine type
            inferred_component = None
            for itm in array:
                if itm is not None:
                    inferred_component = type(itm)
                    break
            if inferred_component is None:
                inferred_component = expected_type
    else:
        # No expected type provided: infer from array contents or element
        if array is not None and len(array) > 0:
            inferred_component = None
            for itm in array:
                if itm is not None:
                    inferred_component = type(itm)
                    break
            if inferred_component is None:
                inferred_component = object
        elif element is not None:
            inferred_component = type(element)
        else:
            inferred_component = object

    new_list = ArrayUtils._copy_list_grow1(array, inferred_component)
    new_list[len(new_list) - 1] = element

    # Perform a relaxed type check: if expected_type given, ensure the element is compatible
    if expected_type is not None and expected_type is not object:
        # If element is not None and not instance of expected_type, raise
        if element is not None and not isinstance(element, expected_type):
            raise TypeError(
                f"Cannot cast element of type {type(element).__name__} to {expected_type.__name__}"
            )
    return new_list