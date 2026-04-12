@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is not None:
        concrete_type = None
        for item in array:
            if item is not None:
                concrete_type = type(item)
                break
    else:
        concrete_type = None
    if concrete_type is None and element is not None:
        concrete_type = type(element)
    if concrete_type is None:
        inferred_type = expected_type if expected_type is not None else object
    else:
        inferred_type = concrete_type
    if expected_type is not None and concrete_type is not None and concrete_type != expected_type:
        raise TypeError(
            f"Cannot cast {concrete_type.__name__} list to {expected_type.__name__} list"
        )
    new_list = ArrayUtils._copy_list_grow1(array, inferred_type)
    new_list[len(new_list) - 1] = element
    return new_list