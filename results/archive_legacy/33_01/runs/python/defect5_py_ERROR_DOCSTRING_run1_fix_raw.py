@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is not None:
        new_list = array.copy()
        new_list.append(element)
    else:
        new_list = [element]
    if expected_type is not None:
        if array is not None:
            if len(array) > 0:
                inferred_component = type(array[0])
            else:
                inferred_component = type(element) if element is not None else object
        else:
            inferred_component = type(element) if element is not None else object
        if inferred_component == object and expected_type != object:
            raise TypeError(f"Cannot cast object list to {expected_type.__name__} list (ClassCastException: [Ljava.lang.Object; cannot be cast to [Ljava.lang.{expected_type.__name__};)")
    return new_list