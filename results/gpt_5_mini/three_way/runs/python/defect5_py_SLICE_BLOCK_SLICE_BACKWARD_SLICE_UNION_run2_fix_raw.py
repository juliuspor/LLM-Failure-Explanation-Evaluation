@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is not None:
        # infer component type from first non-None element if possible
        inferred_type = object
        for item in array:
            if item is not None:
                inferred_type = type(item)
                break
    elif element is not None:
        inferred_type = type(element)
    else:
        inferred_type = object

    new_list = ArrayUtils._copy_list_grow1(array, inferred_type)
    new_list[len(new_list) - 1] = element

    if expected_type is not None:
        # If expected_type specified, ensure element (and existing elements if array provided)
        # are compatible; simulate Java ClassCastException behavior by checking instances.
        if element is not None and not isinstance(element, expected_type):
            raise TypeError(
                f"Cannot cast element of type {type(element).__name__} to {expected_type.__name__}"
            )
        if array is not None:
            for item in array:
                if item is not None and not isinstance(item, expected_type):
                    raise TypeError(
                        f"Cannot cast existing element of type {type(item).__name__} to {expected_type.__name__}"
                    )

    return new_list