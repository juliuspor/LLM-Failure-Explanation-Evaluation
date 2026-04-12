@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is None:
        # start with empty list and append element
        new_list = [element]
        # If expected_type provided, validate element
        if expected_type is not None and element is not None and not isinstance(element, expected_type):
            raise TypeError(
                f"Cannot cast object list to {expected_type.__name__} list (ClassCastException: [Ljava.lang.Object; cannot be cast to [Ljava.lang.{expected_type.__name__};)"
            )
        return new_list

    # array is not None: make a copy and append placeholder
    new_list = array.copy()
    # Validate existing elements against expected_type if provided
    if expected_type is not None:
        for i, item in enumerate(new_list):
            if item is not None and not isinstance(item, expected_type):
                raise TypeError(
                    f"Cannot cast array element at index {i} of type {type(item).__name__} to {expected_type.__name__}"
                )
        # Also validate the element being added
        if element is not None and not isinstance(element, expected_type):
            raise TypeError(
                f"Cannot cast element of type {type(element).__name__} to {expected_type.__name__}"
            )
    # Append the new element
    new_list.append(element)
    return new_list