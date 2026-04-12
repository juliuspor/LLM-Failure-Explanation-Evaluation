@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is None:
        new_list: List[T] = []
    else:
        new_list = array.copy()
    new_list.append(element)

    # If expected_type is provided, ensure all elements conform to it (simulate Java array component type)
    if expected_type is not None and expected_type is not object:
        for i, item in enumerate(new_list):
            if item is None:
                # None is allowed in lists; skip strict type enforcement for None
                continue
            if not isinstance(item, expected_type):
                raise TypeError(
                    f"Cannot cast element at index {i} of type {type(item).__name__} to {expected_type.__name__}"
                )
    return new_list