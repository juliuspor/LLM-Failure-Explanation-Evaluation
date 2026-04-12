@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is not None:
        component_type: Optional[Type] = None
        for item in array:
            if item is not None:
                component_type = type(item)
                break
        if component_type is None:
            if expected_type is not None:
                component_type = expected_type
            else:
                component_type = object
    elif element is not None:
        component_type = type(element)
    elif expected_type is not None:
        component_type = expected_type
    else:
        component_type = object

    if element is not None and component_type is not object:
        if not isinstance(element, component_type):
            raise TypeError(f"Cannot add element of type {type(element).__name__} to list with component type {component_type.__name__}")

    if array is None:
        new_list: List[Any] = [element]
    else:
        new_list = array.copy()
        new_list.append(element)

    if expected_type is not None:
        if component_type is object and expected_type is not object:
            raise TypeError(
                f"Cannot cast object list to {expected_type.__name__} list (ClassCastException: [Ljava.lang.Object; cannot be cast to [Ljava.lang.{expected_type.__name__};)"
            )
    return new_list