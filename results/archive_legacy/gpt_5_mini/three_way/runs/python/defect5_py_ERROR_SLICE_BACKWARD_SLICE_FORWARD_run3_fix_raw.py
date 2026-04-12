@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is not None:
        inferred_element_type = None
        for item in array:
            if item is not None:
                inferred_element_type = type(item)
                break
        if inferred_element_type is None:
            if element is not None:
                inferred_element_type = type(element)
            elif expected_type is not None:
                inferred_element_type = expected_type
            else:
                inferred_element_type = object
    elif element is not None:
        inferred_element_type = type(element)
    elif expected_type is not None:
        inferred_element_type = expected_type
    else:
        inferred_element_type = object

    new_list = ArrayUtils._copy_list_grow1(array, inferred_element_type)
    new_list[len(new_list) - 1] = element

    if expected_type is not None:
        try:
            if inferred_element_type is object and expected_type is not object:
                raise TypeError(
                    f"Cannot cast object list to {expected_type.__name__} list (ClassCastException: [Ljava.lang.Object; cannot be cast to [Ljava.lang.{expected_type.__name__};)"
                )
            if inferred_element_type is not object and expected_type is not object:
                if not (isinstance(inferred_element_type, type) and isinstance(expected_type, type)):
                    pass
                else:
                    if not issubclass(inferred_element_type, expected_type) and not issubclass(expected_type, inferred_element_type):
                        for item in (array or []):
                            if item is not None and not isinstance(item, expected_type):
                                raise TypeError(
                                    f"Cannot cast {inferred_element_type.__name__} list to {expected_type.__name__} list"
                                )
        except TypeError:
            raise
    return new_list