@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is not None:
        component_type = object
        for it in array:
            if it is not None:
                component_type = type(it)
                break
    elif element is not None:
        component_type = type(element)
    else:
        component_type = object
    if array is None:
        new_list: List[T] = [element]
    else:
        new_list = array.copy()
        new_list.append(element)
    if expected_type is not None:
        if element is not None and not isinstance(element, expected_type):
            raise TypeError(
                f"Cannot cast element of type {type(element).__name__} to {expected_type.__name__}"
            )
        if element is None and component_type is object and expected_type != object:
            raise TypeError(
                f"Cannot cast object list to {expected_type.__name__} list (ClassCastException: [Ljava.lang.Object; cannot be cast to [Ljava.lang.{expected_type.__name__};)"
            )
    return new_list