@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is not None and len(array) > 0:
        # infer component type from existing elements if possible
        first_non_none = None
        for itm in array:
            if itm is not None:
                first_non_none = itm
                break
        inferred_component = type(first_non_none) if first_non_none is not None else object
    elif element is not None:
        inferred_component = type(element)
    else:
        inferred_component = object

    new_list = ArrayUtils._copy_list_grow1(array, inferred_component)
    new_list[len(new_list) - 1] = element

    if expected_type is not None:
        # If there are existing elements, ensure they comply with expected_type
        if array is not None:
            for i, itm in enumerate(array):
                if itm is not None and not isinstance(itm, expected_type):
                    raise TypeError(
                        f"Cannot cast list element at index {i} of type {type(itm).__name__} to {expected_type.__name__}"
                    )
        # Also ensure the new element is compatible
        if element is not None and not isinstance(element, expected_type):
            raise TypeError(
                f"Cannot cast element of type {type(element).__name__} to {expected_type.__name__}"
            )

    return new_list