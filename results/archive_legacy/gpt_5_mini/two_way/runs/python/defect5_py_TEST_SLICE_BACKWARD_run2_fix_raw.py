@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    component_type = None
    if expected_type is not None and expected_type is not object:
        component_type = expected_type
    if component_type is None:
        if array is not None:
            for e in array:
                if e is not None:
                    component_type = type(e)
                    break
        if component_type is None and element is not None:
            component_type = type(element)
    if component_type is None:
        component_type = object
    if array is None:
        new_list: List[T] = [None]
    else:
        new_list = array.copy()
        new_list.append(None)
    new_list[len(new_list) - 1] = element
    if expected_type is not None and expected_type is not object:
        for e in (array or []):
            if e is not None and not isinstance(e, expected_type):
                raise TypeError(f"Cannot cast list elements to {expected_type.__name__} list")
        if element is not None and not isinstance(element, expected_type):
            raise TypeError(f"Cannot cast element to {expected_type.__name__} list")
    return new_list