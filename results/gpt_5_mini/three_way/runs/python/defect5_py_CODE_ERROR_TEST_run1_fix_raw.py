@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is not None:
        # infer from existing array elements if possible
        inferred_type = type(array)
    elif expected_type is not None:
        # if no array, but expected_type provided, use it
        inferred_type = expected_type
    elif element is not None:
        inferred_type = type(element)
    else:
        inferred_type = object

    new_list = ArrayUtils._copy_list_grow1(array, inferred_type)
    new_list[len(new_list) - 1] = element

    if expected_type is not None:
        # Only raise if we had an actual array with a concrete element type
        # that is incompatible with expected_type. If array is None, allow
        # creation of a list for the expected_type even if element is None.
        if array is not None:
            # try to determine element types in the existing array
            # if array is empty we cannot infer incompatibility
            if len(array) > 0:
                # check first non-None element
                actual_elem_type = None
                for itm in array:
                    if itm is not None:
                        actual_elem_type = type(itm)
                        break
                if actual_elem_type is not None and actual_elem_type is not expected_type:
                    raise TypeError(
                        f"Cannot cast {actual_elem_type.__name__} list to {expected_type.__name__} list "
                        f"(ClassCastException: [Ljava.lang.{actual_elem_type.__name__}; cannot be cast to "
                        f"[Ljava.lang.{expected_type.__name__};)"
                    )

    return new_list