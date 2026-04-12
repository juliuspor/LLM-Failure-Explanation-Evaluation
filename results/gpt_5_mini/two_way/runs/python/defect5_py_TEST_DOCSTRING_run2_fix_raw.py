@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if expected_type is not None:
        # If array provided, ensure existing elements are compatible with expected_type
        if array is not None:
            for i, v in enumerate(array):
                if v is not None and not isinstance(v, expected_type):
                    raise TypeError(
                        f"Cannot cast element at index {i} of type {type(v).__name__} to {expected_type.__name__}"
                    )
        # Ensure the new element is compatible
        if element is not None and not isinstance(element, expected_type):
            raise TypeError(
                f"Cannot add element of type {type(element).__name__} to {expected_type.__name__} list"
            )
        # If both array and element are None, we cannot determine component type -> simulate cast failure
        if array is None and element is None and expected_type is not object:
            raise TypeError(
                f"Cannot cast object list to {expected_type.__name__} list (ClassCastException: [Ljava.lang.Object; cannot be cast to [Ljava.lang.{expected_type.__name__};)"
            )

    # Build the new list functionally
    if array is None:
        new_list: List[T] = []
    else:
        new_list = array.copy()
    new_list.append(element)
    return new_list