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
        # Only enforce type checks for non-None elements. None is allowed as a placeholder.
        for idx, val in enumerate(new_list):
            if val is not None and not isinstance(val, expected_type):
                raise TypeError(
                    f"Cannot cast element at index {idx} of type {type(val).__name__} to {expected_type.__name__} "
                    f"(ClassCastException: [Ljava.lang.{type(val).__name__}; cannot be cast to [Ljava.lang.{expected_type.__name__};)"
                )

    return new_list