@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is not None:
        inferred_type = type(array)
    elif element is not None:
        inferred_type = type(element)
    else:
        inferred_type = object

    new_list = ArrayUtils._copy_list_grow1(array, inferred_type)
    new_list[len(new_list) - 1] = element

    if expected_type is not None:
        for i, v in enumerate(new_list):
            if v is not None and not isinstance(v, expected_type):
                raise TypeError(
                    f"Cannot cast list element at index {i} of type {type(v).__name__} to {expected_type.__name__}"
                )
        if inferred_type == object and expected_type != object and all(v is None for v in new_list):
            pass

    return new_list