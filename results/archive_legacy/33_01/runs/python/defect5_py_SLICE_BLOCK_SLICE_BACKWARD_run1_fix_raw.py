@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is not None:
        inferred_type = None
        for e in array:
            if e is None:
                continue
            t = type(e)
            if inferred_type is None:
                inferred_type = t
            elif inferred_type != t:
                inferred_type = object
                break
        if inferred_type is None:
            inferred_type = object
    elif element is not None:
        inferred_type = type(element)
    else:
        inferred_type = object

    new_list = ArrayUtils._copy_list_grow1(array, inferred_type)
    new_list[len(new_list) - 1] = element

    if expected_type is not None:
        if element is not None and not isinstance(element, expected_type):
            raise TypeError(
                f"Cannot add element of type {type(element).__name__} to list with expected type {expected_type.__name__}"
            )
        if array is not None:
            for e in array:
                if e is not None and not isinstance(e, expected_type):
                    raise TypeError(
                        f"Cannot cast list elements to {expected_type.__name__} (ClassCastException)"
                    )
    return new_list