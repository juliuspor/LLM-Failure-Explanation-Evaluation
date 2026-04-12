@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is not None:
        if len(array) == 0:
            inferred_element_type = object
        else:
            inferred_element_type = None
            for x in array:
                if x is None:
                    continue
                t = type(x)
                if inferred_element_type is None:
                    inferred_element_type = t
                elif inferred_element_type != t:
                    inferred_element_type = object
                    break
            if inferred_element_type is None:
                inferred_element_type = object
    elif element is not None:
        inferred_element_type = type(element)
    else:
        inferred_element_type = object

    new_list = ArrayUtils._copy_list_grow1(array, inferred_element_type)
    new_list[len(new_list) - 1] = element

    if expected_type is not None:
        if inferred_element_type == object:
            for i, v in enumerate(new_list):
                if v is None:
                    continue
                if not isinstance(v, expected_type):
                    try:
                        new_list[i] = expected_type(v)
                    except Exception:
                        raise TypeError(f"Element at index {i} of type {type(v).__name__} cannot be converted to {expected_type.__name__}")
        else:
            if not issubclass(inferred_element_type, expected_type) and inferred_element_type is not object:
                raise TypeError(f"Cannot cast {inferred_element_type.__name__} list to {expected_type.__name__} list")

    return new_list