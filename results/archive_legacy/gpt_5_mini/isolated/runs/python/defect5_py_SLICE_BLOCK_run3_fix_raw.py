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
        if inferred_type == object and expected_type != object:
            items_to_check = []
            if array is not None:
                items_to_check = array
            elif element is not None:
                items_to_check = [element]
            bad_indices = []
            for i, e in enumerate(items_to_check):
                if e is not None and not isinstance(e, expected_type):
                    bad_indices.append(i)
            if bad_indices:
                raise TypeError(f"List contains elements not of {expected_type.__name__} at indices {bad_indices}")
    return new_list