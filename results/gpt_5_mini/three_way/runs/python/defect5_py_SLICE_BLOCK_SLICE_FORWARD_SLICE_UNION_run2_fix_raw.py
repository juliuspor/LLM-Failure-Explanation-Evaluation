@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is not None:
        # infer element type from existing array contents if possible
        inferred_elem_type = None
        for item in array:
            if item is not None:
                inferred_elem_type = type(item)
                break
        if inferred_elem_type is None:
            inferred_type = object
        else:
            inferred_type = inferred_elem_type
    elif element is not None:
        inferred_type = type(element)
    else:
        inferred_type = object

    new_list = ArrayUtils._copy_list_grow1(array, inferred_type)
    new_list[len(new_list) - 1] = element

    if expected_type is not None:
        # Only enforce type check when we have a concrete element to check
        if element is not None and not isinstance(element, expected_type):
            raise TypeError(
                f"Cannot cast element of type {type(element).__name__} to {expected_type.__name__} "
                f"(ClassCastException: {type(element).__name__} cannot be cast to {expected_type.__name__})"
            )
    return new_list