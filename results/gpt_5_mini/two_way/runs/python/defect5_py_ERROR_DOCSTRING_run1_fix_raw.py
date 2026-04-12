@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is None:
        new_list: List[T] = []
    else:
        new_list = array.copy()
    # If expected_type is given, validate existing elements and the new element
    if expected_type is not None:
        # Validate existing elements
        for i, item in enumerate(new_list):
            if item is not None and not isinstance(item, expected_type):
                raise TypeError(
                    f"Existing element at index {i} of type {type(item).__name__} cannot be cast to {expected_type.__name__}"
                )
        # Validate the element to add
        if element is not None and not isinstance(element, expected_type):
            raise TypeError(
                f"Element of type {type(element).__name__} cannot be cast to {expected_type.__name__}"
            )
    new_list.append(element)
    return new_list