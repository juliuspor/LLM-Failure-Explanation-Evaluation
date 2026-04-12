@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is not None:
        if len(array) > 0:
            inferred_type = type(array[0])
        else:
            inferred_type = object
    elif element is not None:
        inferred_type = type(element)
    else:
        inferred_type = object

    new_list = ArrayUtils._copy_list_grow1(array, inferred_type)
    new_list[len(new_list) - 1] = element

    if expected_type is not None and expected_type is not object:
        if inferred_type is object:
            if array is None and element is None:
                raise TypeError(
                    f"Cannot cast object list to {expected_type.__name__} list (ClassCastException: [Ljava.lang.Object; cannot be cast to [Ljava.lang.{expected_type.__name__};)"
                )
        else:
            try:
                if not issubclass(inferred_type, expected_type):
                    raise TypeError(
                        f"Cannot cast {inferred_type.__name__} list to {expected_type.__name__} list"
                    )
            except TypeError:
                if not isinstance(element, expected_type) if element is not None else True:
                    raise TypeError(
                        f"Element of type {type(element).__name__} is not instance of {expected_type.__name__}"
                    )
    return new_list