@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is not None:
        new_list = array.copy()
        new_list.append(element)
    elif element is not None:
        new_list = [element]
    else:
        new_list = []

    if expected_type is not None:
        # Simulate Java array type checking
        for item in new_list:
            if item is not None and not isinstance(item, expected_type):
                raise TypeError(
                    f"Cannot cast object list to {expected_type.__name__} list "
                    f"(ClassCastException: [Ljava.lang.Object; cannot be cast to "
                    f"[Ljava.lang.{expected_type.__name__};)"
                )
    
    return new_list
