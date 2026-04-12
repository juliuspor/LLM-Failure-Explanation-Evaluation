@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is not None:
        # Infer element type from contents (ignore None)
        inferred_elem_type = None
        for item in array:
            if item is not None:
                inferred_elem_type = type(item)
                break
        if inferred_elem_type is None and element is not None:
            inferred_elem_type = type(element)
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
        # Validate or attempt to coerce each non-None element to expected_type
        for i, val in enumerate(new_list):
            if val is None:
                continue
            if not isinstance(val, expected_type):
                try:
                    new_list[i] = expected_type(val)
                except Exception:
                    raise TypeError(
                        f"Cannot cast element at index {i} of type {type(val).__name__} to {expected_type.__name__}"
                    )
    return new_list