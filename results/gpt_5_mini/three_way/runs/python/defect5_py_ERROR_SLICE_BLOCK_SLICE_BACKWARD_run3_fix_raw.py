@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is None:
        # Start from empty list; just validate the single element if expected_type provided
        if expected_type is not None and element is not None and not isinstance(element, expected_type):
            raise TypeError(
                f"Element of type {type(element).__name__} cannot be added to list of {expected_type.__name__}"
            )
        return [element]

    # array is not None
    # Validate existing elements against expected_type if provided
    if expected_type is not None:
        for i, item in enumerate(array):
            if item is not None and not isinstance(item, expected_type):
                raise TypeError(
                    f"Array element {i} of type {type(item).__name__} is not compatible with {expected_type.__name__}"
                )
        if element is not None and not isinstance(element, expected_type):
            raise TypeError(
                f"Element of type {type(element).__name__} is not compatible with {expected_type.__name__}"
            )

    new_list = ArrayUtils._copy_list_grow1(array, None)
    new_list[len(new_list) - 1] = element
    return new_list