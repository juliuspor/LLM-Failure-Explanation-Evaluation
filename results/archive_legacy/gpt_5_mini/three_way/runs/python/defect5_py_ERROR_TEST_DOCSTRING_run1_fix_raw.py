@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is not None:
        result = array.copy()
        result.append(element)
        return result
    component_type = None
    if expected_type is not None:
        component_type = expected_type
    if element is not None:
        component_type = type(element)
    new_list = [None]
    new_list[0] = element
    return new_list