@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if expected_type is not None:
        component_type = expected_type
    else:
        if array is not None:
            component_type = object
            for x in array:
                if x is not None:
                    component_type = type(x)
                    break
        elif element is not None:
            component_type = type(element)
        else:
            component_type = object
    new_list = ArrayUtils._copy_list_grow1(array, component_type)
    new_list[len(new_list) - 1] = element
    return new_list