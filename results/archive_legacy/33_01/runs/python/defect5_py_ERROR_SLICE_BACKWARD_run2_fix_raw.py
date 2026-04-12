@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is not None:
        inferred_type = object
        for item in array:
            if item is not None:
                inferred_type = type(item)
                break
    elif element is not None:
        inferred_type = type(element)
    else:
        inferred_type = object

    new_list = ArrayUtils._copy_list_grow1(array, inferred_type)
    new_list[len(new_list) - 1] = element

    if expected_type is not None:
        if expected_type != object:
            if inferred_type == object:
                for item in new_list:
                    if item is not None and not isinstance(item, expected_type):
                        raise TypeError(
                            f"Cannot cast object list to {expected_type.__name__} list (ClassCastException: [Ljava.lang.Object; cannot be cast to [Ljava.lang.{expected_type.__name__};)"
                        )
            else:
                if not issubclass(inferred_type, expected_type):
                    raise TypeError(
                        f"Cannot cast {inferred_type.__name__} list to {expected_type.__name__} list (ClassCastException)"
                    )
    return new_list