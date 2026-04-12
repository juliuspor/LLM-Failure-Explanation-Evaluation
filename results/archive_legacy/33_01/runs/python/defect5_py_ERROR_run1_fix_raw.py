@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is None:
        if element is None:
            inferred_type = object
            new_list = [None]
            new_list[0] = element
        else:
            inferred_type = type(element)
            new_list = [element]
    else:
        inferred_type = object
        for item in array:
            if item is not None:
                inferred_type = type(item)
                break
        new_list = array.copy()
        new_list.append(element)
    if expected_type is not None:
        if inferred_type == object and expected_type != object:
            raise TypeError(
                f"Cannot cast object list to {expected_type.__name__} list (ClassCastException: [Ljava.lang.Object; cannot be cast to [Ljava.lang.{expected_type.__name__};)"
            )
    return new_list