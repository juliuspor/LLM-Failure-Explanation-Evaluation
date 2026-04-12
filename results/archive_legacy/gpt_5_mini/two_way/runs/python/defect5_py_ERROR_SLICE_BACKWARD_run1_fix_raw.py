@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is None:
        if expected_type is not None and element is not None and not isinstance(element, expected_type):
            raise TypeError(f"Element of type {type(element).__name__} cannot be added to list of {expected_type.__name__}")
        return [element]
    result = array.copy()
    if expected_type is not None:
        for i, e in enumerate(result):
            if e is not None and not isinstance(e, expected_type):
                raise TypeError(f"Cannot cast element at index {i} of type {type(e).__name__} to {expected_type.__name__}")
        if element is not None and not isinstance(element, expected_type):
            raise TypeError(f"Element of type {type(element).__name__} cannot be added to list of {expected_type.__name__}")
    result.append(element)
    return result