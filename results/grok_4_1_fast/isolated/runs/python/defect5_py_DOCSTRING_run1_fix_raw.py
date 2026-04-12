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
    new_list_element_type = None
    if array is not None:
        new_list = ArrayUtils._copy_list_grow1(array, type(array))
    else:
        new_list = ArrayUtils._copy_list_grow1(None, None)
    
    new_list[len(new_list) - 1] = element
    
    if expected_type is not None:
        inferred_type = type(array[0]) if array and array else type(element) if element is not None else object
        if inferred_type == object and expected_type != object:
            raise TypeError(
                f"Cannot cast object list to {expected_type.__name__} list "
                f"(ClassCastException: [Ljava.lang.Object; cannot be cast to "
                f"[Ljava.lang.{expected_type.__name__};)"
            )
    
    return new_list