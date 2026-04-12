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
        # Allow None elements regardless of expected_type
        if element is not None:
            # If element is concrete, ensure it's an instance of expected_type
            if not isinstance(element, expected_type):
                raise TypeError(
                    f"Cannot add element of type {type(element).__name__} to {expected_type.__name__} list"
                )
        else:
            # element is None. If array provides concrete element types, ensure compatibility
            if array is not None:
                # find first non-None element to infer element type
                for e in array:
                    if e is not None:
                        if not isinstance(e, expected_type):
                            raise TypeError(
                                f"Cannot cast list element of type {type(e).__name__} to {expected_type.__name__}"
                            )
                        break
            # otherwise both array and element are None: allowed

    return new_list