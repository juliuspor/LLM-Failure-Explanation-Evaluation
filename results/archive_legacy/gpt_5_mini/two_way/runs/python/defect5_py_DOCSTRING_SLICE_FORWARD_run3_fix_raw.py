@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if expected_type is not None and not isinstance(expected_type, type):
        raise TypeError("expected_type must be a concrete class")
    if array is None:
        if expected_type is not None and element is not None and not isinstance(element, expected_type):
            raise TypeError(f"Cannot add element of type {type(element).__name__} to list of {expected_type.__name__}")
        return [element]
    if expected_type is not None:
        for i, item in enumerate(array):
            if item is not None and not isinstance(item, expected_type):
                raise TypeError(f"Array element {i} is of type {type(item).__name__}, expected {expected_type.__name__}")
        if element is not None and not isinstance(element, expected_type):
            raise TypeError(f"Cannot add element of type {type(element).__name__} to list of {expected_type.__name__}")
    new_list = array.copy()
    new_list.append(element)
    return new_list