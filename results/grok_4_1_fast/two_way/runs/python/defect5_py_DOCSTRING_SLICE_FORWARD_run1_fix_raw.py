@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is None:
        new_list = []
    else:
        new_list = array.copy()
    new_list.append(element)
    
    if expected_type is not None:
        inferred_type = type(array[0]) if array and array[0] is not None else type(element) if element is not None else object
        if inferred_type == object and expected_type != object:
            raise TypeError(
                f"Cannot cast object list to {expected_type.__name__} list "
                f"(ClassCastException: [Ljava.lang.Object; cannot be cast to "
                f"[Ljava.lang.{expected_type.__name__};)"
            )
    
    return new_list