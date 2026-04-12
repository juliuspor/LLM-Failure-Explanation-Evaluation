@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is None:
        # start with empty list
        new_list: List[T] = []
    else:
        # copy existing elements to a new list to avoid mutating input
        new_list = array.copy()
    # If expected_type specified, validate existing elements and the new element
    if expected_type is not None:
        for i, item in enumerate(new_list):
            if item is not None and not isinstance(item, expected_type):
                raise TypeError(
                    f"Cannot cast element at index {i} of type {type(item).__name__} to {expected_type.__name__}"
                )
        if element is not None and not isinstance(element, expected_type):
            raise TypeError(
                f"Cannot cast element of type {type(element).__name__} to {expected_type.__name__}"
            )
    new_list.append(element)
    return new_list