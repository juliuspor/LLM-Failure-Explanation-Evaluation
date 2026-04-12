@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is not None:
        inferred_type = type(array)
    elif element is not None:
        inferred_type = type(element)
    else:
        inferred_type = object

    new_list = ArrayUtils._copy_list_grow1(array, inferred_type)
    new_list[len(new_list) - 1] = element

    if expected_type is not None:
        # If the array itself was an untyped/object list, try to ensure element compatibility
        if inferred_type == object and expected_type != object:
            # If element is present and not compatible with expected_type, raise
            if element is not None and not isinstance(element, expected_type):
                raise TypeError(
                    f"Cannot cast element of type {type(element).__name__} to {expected_type.__name__}"
                )
            # Otherwise, we won't raise: Python lists are heterogeneous; mimic Java behavior
            # by returning the list (no actual array type to enforce in Python)
        else:
            # If array had a concrete type different from expected_type, ensure compatibility of elements
            if array is not None and expected_type != object:
                # Check existing elements for compatibility
                for i, itm in enumerate(array):
                    if itm is not None and not isinstance(itm, expected_type):
                        raise TypeError(
                            f"Existing element at index {i} of type {type(itm).__name__} cannot be cast to {expected_type.__name__}"
                        )
            # Also check the new element
            if element is not None and not isinstance(element, expected_type):
                raise TypeError(
                    f"Cannot cast element of type {type(element).__name__} to {expected_type.__name__}"
                )

    return new_list