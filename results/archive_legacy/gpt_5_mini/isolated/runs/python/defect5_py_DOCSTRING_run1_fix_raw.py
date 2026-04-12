@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is None:
        new_list = [element]
    else:
        new_list = array.copy()
        new_list.append(element)
    if expected_type is not None:
        if element is not None and not isinstance(element, expected_type):
            raise TypeError(f"Element of type {type(element).__name__} cannot be cast to {expected_type.__name__}")
        if array is not None:
            for i, v in enumerate(array):
                if v is not None and not isinstance(v, expected_type):
                    raise TypeError(f"Element at index {i} of type {type(v).__name__} cannot be cast to {expected_type.__name__}")
    return new_list