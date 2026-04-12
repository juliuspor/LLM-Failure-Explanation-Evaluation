@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is not None:
        new_list = ArrayUtils._copy_list_grow1(array, type(array))
    else:
        new_list = ArrayUtils._copy_list_grow1(None, type(element) if element is not None else object)
    new_list[len(new_list) - 1] = element

    if expected_type is not None and element is not None:
        if not isinstance(element, expected_type):
            raise TypeError(
                f"Cannot add element of type {type(element).__name__} to list of expected type {expected_type.__name__}"
            )
    return new_list