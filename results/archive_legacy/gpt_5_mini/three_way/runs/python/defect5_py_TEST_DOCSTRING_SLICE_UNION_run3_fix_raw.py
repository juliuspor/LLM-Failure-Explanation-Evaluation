@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is not None and len(array) > 0:
        inferred_element_type = type(array[0])
    elif element is not None:
        inferred_element_type = type(element)
    else:
        inferred_element_type = object

    if expected_type is not None:
        effective_type = expected_type
    else:
        effective_type = inferred_element_type

    if element is not None and effective_type is not object and not isinstance(element, effective_type):
        raise TypeError(
            f"Cannot cast element of type {type(element).__name__} to {effective_type.__name__}"
        )

    if array is not None and effective_type is not object:
        for i, x in enumerate(array):
            if x is not None and not isinstance(x, effective_type):
                raise TypeError(
                    f"Array element {i} is of type {type(x).__name__} which cannot be cast to {effective_type.__name__}"
                )

    new_list = ArrayUtils._copy_list_grow1(array, effective_type)
    new_list[len(new_list) - 1] = element
    return new_list