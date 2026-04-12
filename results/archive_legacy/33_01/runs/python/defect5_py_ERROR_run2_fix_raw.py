@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is not None:
        if len(array) > 0:
            component_type = type(array[0])
        else:
            component_type = expected_type if expected_type is not None else (type(element) if element is not None else object)
    else:
        component_type = type(element) if element is not None else object
    new_list = ArrayUtils._copy_list_grow1(array, component_type)
    new_list[len(new_list) - 1] = element
    if expected_type is not None:
        if element is not None and not isinstance(element, expected_type):
            raise TypeError(
                f"Cannot cast object list to {expected_type.__name__} list (ClassCastException: [Ljava.lang.Object; cannot be cast to [Ljava.lang.{expected_type.__name__};)"
            )
        if array is not None:
            for i, el in enumerate(array):
                if el is not None and not isinstance(el, expected_type):
                    raise TypeError(
                        f"Cannot cast object list to {expected_type.__name__} list (ClassCastException: [Ljava.lang.Object; cannot be cast to [Ljava.lang.{expected_type.__name__};)"
                    )
    return new_list