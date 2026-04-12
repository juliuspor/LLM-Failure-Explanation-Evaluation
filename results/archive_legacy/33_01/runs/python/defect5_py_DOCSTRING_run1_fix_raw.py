@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is None:
        new_list = [element]
    else:
        new_list = array.copy()
        new_list.append(element)
    if expected_type is not None:
        if element is not None and not isinstance(element, expected_type):
            raise TypeError(
                f"Cannot cast element of type {type(element).__name__} to {expected_type.__name__}"
            )
        if array is not None:
            for idx, item in enumerate(array):
                if item is not None and not isinstance(item, expected_type):
                    raise TypeError(
                        f"Cannot cast element at index {idx} of type {type(item).__name__} to {expected_type.__name__}"
                    )
    return new_list