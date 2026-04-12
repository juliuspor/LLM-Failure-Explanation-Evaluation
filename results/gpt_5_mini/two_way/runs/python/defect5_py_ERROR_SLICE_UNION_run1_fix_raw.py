@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if expected_type is not None:
        # Validate existing array elements (if any) are compatible with expected_type
        if array is not None:
            for i, v in enumerate(array):
                if v is not None and not isinstance(v, expected_type):
                    raise TypeError(
                        f"Cannot cast list element at index {i} of type {type(v).__name__} to {expected_type.__name__}"
                    )
        # Validate the new element
        if element is not None and not isinstance(element, expected_type):
            raise TypeError(
                f"Cannot cast element of type {type(element).__name__} to {expected_type.__name__}"
            )
    # Create new list functionally (do not modify input)
    if array is None:
        return [element]
    new_list = array.copy()
    new_list.append(element)
    return new_list