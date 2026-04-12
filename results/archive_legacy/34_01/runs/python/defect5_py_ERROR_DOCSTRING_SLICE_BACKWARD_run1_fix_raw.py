@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is not None:
        inferred_type = object
        for item in array:
            if item is not None:
                inferred_type = type(item)
                break
    elif element is not None:
        inferred_type = type(element)
    else:
        inferred_type = object
    if expected_type is not None and inferred_type == object and expected_type != object:
        raise TypeError(
            f"Cannot cast object list to {expected_type.__name__} list (ClassCastException: [Ljava.lang.Object; cannot be cast to [Ljava.lang.{expected_type.__name__};)"
        )
    if array is None:
        new_list: List[T] = [element]
    else:
        new_list = array.copy()
        new_list.append(element)
    return new_list