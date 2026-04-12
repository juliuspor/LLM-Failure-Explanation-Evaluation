@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is None:
        # start from empty list
        result: List[T] = []
    else:
        result = array.copy()

    # Validate expected_type if provided
    if expected_type is not None and element is not None and not isinstance(element, expected_type):
        raise TypeError(
            f"Cannot add element of type {type(element).__name__} to list of {expected_type.__name__}"
        )

    result.append(element)

    return result