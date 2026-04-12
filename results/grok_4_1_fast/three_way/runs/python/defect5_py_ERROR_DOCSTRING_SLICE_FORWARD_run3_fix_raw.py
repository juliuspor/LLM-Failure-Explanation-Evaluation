@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is None or len(array) == 0:
        if expected_type is not None and element is not None and not isinstance(element, expected_type):
            raise TypeError(f"Element {element} is not of type {expected_type.__name__}")
        return [element]
    
    # Infer element type from array
    element_types = set(type(item) for item in array if item is not None)
    if element is not None:
        element_types.add(type(element))
    
    if expected_type is not None and element_types and expected_type not in element_types:
        raise TypeError(
            f"Cannot cast to {expected_type.__name__} list - contains {list(element_types)}"
            f" (ClassCastException: [Ljava.lang.Object; cannot be cast to "
            f"[Ljava.lang.{expected_type.__name__};)"
        )
    
    new_list = array.copy()
    new_list.append(element)
    return new_list
