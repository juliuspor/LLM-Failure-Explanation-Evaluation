@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is None:
        result: List[T] = [element]
    else:
        result = array.copy()
        result.append(element)

    if expected_type is not None:
        # If element is not None, ensure it matches expected_type
        if element is not None and not isinstance(element, expected_type):
            raise TypeError(
                f"Cannot cast element of type {type(element).__name__} to {expected_type.__name__} "
                f"(ClassCastException: {type(element).__name__} cannot be cast to {expected_type.__name__})"
            )
        # If element is None and array existed, we can try to infer component type from array
        if element is None and array is not None and len(array) > 0:
            first = array[0]
            if first is not None and not isinstance(first, expected_type):
                raise TypeError(
                    f"Cannot cast array elements to {expected_type.__name__} list "
                    f"(ClassCastException: {type(first).__name__} cannot be cast to {expected_type.__name__})"
                )

    return result