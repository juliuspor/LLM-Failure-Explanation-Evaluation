@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is not None:
        comp_type = None
        for e in array:
            if e is not None:
                comp_type = type(e)
                break
        if comp_type is None:
            comp_type = object
    elif element is not None:
        comp_type = type(element)
    else:
        comp_type = object
    new_list = ArrayUtils._copy_list_grow1(array, comp_type)
    new_list[len(new_list) - 1] = element
    if expected_type is not None:
        if comp_type is object:
            if element is None:
                raise TypeError(f"Cannot cast object list to {expected_type.__name__} list (unknown element type)")
            if not isinstance(element, expected_type):
                raise TypeError(
                    f"Cannot cast object list to {expected_type.__name__} list (element of type {type(element).__name__} is not {expected_type.__name__})"
                )
        else:
            if not issubclass(comp_type, expected_type) and not issubclass(expected_type, comp_type):
                if element is not None and not isinstance(element, expected_type):
                    raise TypeError(
                        f"Cannot cast {comp_type.__name__} list to {expected_type.__name__} list"
                    )
    return new_list