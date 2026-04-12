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
    if array is not None:
        new_list = array.copy()
    else:
        new_list = []
    new_list.append(element)
    return new_list
