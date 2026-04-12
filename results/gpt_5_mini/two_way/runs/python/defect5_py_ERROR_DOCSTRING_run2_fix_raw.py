@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if expected_type is not None:
        # Validate existing elements when array provided
        if array is not None:
            for i, item in enumerate(array):
                if item is not None and not isinstance(item, expected_type):
                    raise TypeError(
                        f"Cannot cast element at index {i} of type {type(item).__name__} to {expected_type.__name__}"
                    )
        # Validate the element to add
        if element is not None and not isinstance(element, expected_type):
            raise TypeError(
                f"Cannot cast element of type {type(element).__name__} to {expected_type.__name__}"
            )
    # Create new list copying elements (if any) and append the element
    if array is None:
        new_list: List[T] = []
    else:
        new_list = array.copy()
    new_list.append(element)
    return new_list