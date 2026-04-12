@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is not None:
        inferred_type = object
        for item in array:
            if item is not None:
                inferred_type = type(item)
                break
        if inferred_type is not object:
            for item in array:
                if item is not None and type(item) is not inferred_type:
                    inferred_type = object
                    break
    elif element is not None:
        inferred_type = type(element)
    else:
        inferred_type = object

    if expected_type is not None:
        if inferred_type is object:
            if array is not None:
                for item in array:
                    if item is not None and not isinstance(item, expected_type):
                        raise TypeError(f"Array contains elements that are not of type {expected_type.__name__}")
            if element is not None and not isinstance(element, expected_type):
                raise TypeError(f"Element is not of type {expected_type.__name__}")
        else:
            if not issubclass(inferred_type, expected_type):
                raise TypeError(f"Cannot cast {inferred_type.__name__} list to {expected_type.__name__} list")

    new_list = ArrayUtils._copy_list_grow1(array, inferred_type)
    new_list[len(new_list) - 1] = element
    return new_list