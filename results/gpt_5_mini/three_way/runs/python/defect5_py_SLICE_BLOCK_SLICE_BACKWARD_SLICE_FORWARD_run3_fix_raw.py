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
        # If we only have the generic object type inferred (no concrete array or element),
        # allow the operation instead of rejecting it — Python lists are dynamic.
        if inferred_type is object:
            pass
        else:
            # If array provided, ensure its existing elements are compatible with expected_type.
            # If any existing non-None element is not an instance of expected_type, raise.
            if array is not None:
                for i, itm in enumerate(array):
                    if itm is not None and not isinstance(itm, expected_type):
                        raise TypeError(
                            f"Cannot cast list element at index {i} of type {type(itm).__name__} to {expected_type.__name__}"
                        )
            # Also check the new element
            if element is not None and not isinstance(element, expected_type):
                raise TypeError(
                    f"Cannot cast element of type {type(element).__name__} to {expected_type.__name__}"
                )

    return new_list