@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is not None:
        new_list = array.copy()
        new_list.append(element)
    else:
        new_list = [element]
    if expected_type is not None and element is not None and not isinstance(element, expected_type):
        raise TypeError(
            f"Cannot cast object list to {expected_type.__name__} list (ClassCastException: [Ljava.lang.Object; cannot be cast to [Ljava.lang.{expected_type.__name__};)"
        )
    return new_list