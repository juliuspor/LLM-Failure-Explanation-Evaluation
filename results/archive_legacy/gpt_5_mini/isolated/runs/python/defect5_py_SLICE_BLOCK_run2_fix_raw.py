@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is not None:
        inferred_type = None
        for el in array:
            if el is not None:
                inferred_type = type(el)
                break
        if inferred_type is None:
            inferred_type = object
    elif element is not None:
        inferred_type = type(element)
    else:
        inferred_type = object

    new_list = ArrayUtils._copy_list_grow1(array, inferred_type)
    new_list[len(new_list) - 1] = element

    if expected_type is not None:
        if inferred_type is object:
            all_ok = True
            if array is not None:
                for el in array:
                    if el is not None and not isinstance(el, expected_type):
                        all_ok = False
                        break
            if element is not None and not isinstance(element, expected_type):
                all_ok = False
            if not all_ok:
                raise TypeError(f"Cannot cast object list to {expected_type.__name__} list (incompatible element types)")
        else:
            if not issubclass(inferred_type, expected_type):
                if array is not None:
                    for el in array:
                        if el is not None and not isinstance(el, expected_type):
                            raise TypeError(f"Cannot cast {inferred_type.__name__} list to {expected_type.__name__} list (incompatible element types)")
                if element is not None and not isinstance(element, expected_type):
                    raise TypeError(f"Cannot cast {inferred_type.__name__} list to {expected_type.__name__} list (incompatible element types)")
    return new_list