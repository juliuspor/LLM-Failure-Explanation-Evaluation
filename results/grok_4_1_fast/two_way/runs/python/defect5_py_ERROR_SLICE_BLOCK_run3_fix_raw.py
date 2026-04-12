@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    """
    Return a new list with `element` appended.

    This is a functional-style helper: the input list is not modified. If
    `array` is None, it is treated as an empty list.

    Args:
        array: Source list (may be None).
        element: Element to append.
        expected_type: Optional expected element type used to mirror Java-style
            component type checks in this translated code.
        
    Returns:
        A new list containing the original elements followed by `element`.
        
    Raises:
        TypeError: If `expected_type` is provided and the operation simulates a
            Java array cast failure.
    """
    # Infer element type from existing list or new element
    if array is not None and len(array) > 0:
        # Find first non-None element to infer type
        for item in array:
            if item is not None:
                inferred_type = type(item)
                break
        else:
            inferred_type = type(element) if element is not None else object
    elif element is not None:
        inferred_type = type(element)
    else:
        inferred_type = object
    
    new_list = ArrayUtils._copy_list_grow1(array, inferred_type)
    new_list[len(new_list) - 1] = element
    
    if expected_type is not None and inferred_type != object and not issubclass(inferred_type, expected_type):
        raise TypeError(
            f"Cannot cast {inferred_type.__name__} list to {expected_type.__name__} list "
            f"(ClassCastException: [L{inferred_type.__module__}.{inferred_type.__name__}; "
            f"cannot be cast to [L{expected_type.__module__}.{expected_type.__name__};)"
        )
    
    return new_list
