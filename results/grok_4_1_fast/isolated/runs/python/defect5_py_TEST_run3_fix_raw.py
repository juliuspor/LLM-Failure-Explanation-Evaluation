@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is None:
        new_list = []
    else:
        new_list = array.copy()
    new_list.append(element)
    
    if expected_type is not None and element is not None:
        if not isinstance(element, expected_type):
            raise TypeError(
                f"Cannot cast object list to {expected_type.__name__} list "
                f"(ClassCastException: [Ljava.lang.Object; cannot be cast to "
                f"[Ljava.lang.{expected_type.__name__};)"
            )
    
    return new_list