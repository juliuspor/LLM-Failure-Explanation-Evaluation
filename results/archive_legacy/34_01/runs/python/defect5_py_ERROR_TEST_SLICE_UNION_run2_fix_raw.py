@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is not None:
        inferred_type = type(array)
    elif element is not None:
        inferred_type = type(element)
    elif expected_type is not None and expected_type != object:
        inferred_type = expected_type
    else:
        inferred_type = object

    if expected_type is not None and inferred_type == object and expected_type != object:
        inferred_type = expected_type

    new_list = ArrayUtils._copy_list_grow1(array, inferred_type)
    new_list[len(new_list) - 1] = element

    return new_list