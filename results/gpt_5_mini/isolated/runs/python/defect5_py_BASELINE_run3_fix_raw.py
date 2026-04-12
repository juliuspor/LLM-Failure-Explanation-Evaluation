@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is not None and len(array) > 0:
        # infer component type from first non-None element if possible
        inferred_comp_type = None
        for item in array:
            if item is not None:
                inferred_comp_type = type(item)
                break
        if inferred_comp_type is None:
            # all elements are None, fall back to expected_type or object
            inferred_comp_type = expected_type if expected_type is not None else object
    elif element is not None:
        inferred_comp_type = type(element)
    else:
        inferred_comp_type = expected_type if expected_type is not None else object

    new_list = ArrayUtils._copy_list_grow1(array, inferred_comp_type)
    new_list[len(new_list) - 1] = element

    if expected_type is not None:
        # allow if expected_type is object or inferred is object (unknown) or types match
        if inferred_comp_type is not object and not issubclass(inferred_comp_type, expected_type) and inferred_comp_type != expected_type:
            raise TypeError(
                f"Cannot cast list of {inferred_comp_type.__name__} to {expected_type.__name__} list"
            )

    return new_list