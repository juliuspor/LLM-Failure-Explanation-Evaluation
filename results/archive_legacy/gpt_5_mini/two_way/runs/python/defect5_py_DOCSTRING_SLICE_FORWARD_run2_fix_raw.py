@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is None:
        result = []
    else:
        result = list(array)
    if expected_type is not None:
        if element is not None and not isinstance(element, expected_type):
            raise TypeError(f"element {element!r} is not of expected type {expected_type.__name__}")
        for i, item in enumerate(result):
            if item is not None and not isinstance(item, expected_type):
                raise TypeError(f"array element at index {i} {item!r} is not of expected type {expected_type.__name__}")
    result.append(element)
    return result