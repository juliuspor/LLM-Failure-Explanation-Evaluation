@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is None:
        new_list: List[T] = [element]
    else:
        new_list = array.copy()
        new_list.append(element)
    if expected_type is not None:
        if not all((e is None or isinstance(e, expected_type)) for e in new_list):
            raise TypeError(f"Cannot cast object list to {expected_type.__name__} list (ClassCastException: [Ljava.lang.Object; cannot be cast to [Ljava.lang.{expected_type.__name__};)")
    return new_list