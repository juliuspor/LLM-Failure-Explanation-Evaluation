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
        if inferred_type == object and expected_type != object:
            if array is None or len(array) == 0:
                inferred_type = expected_type
            else:
                for item in array:
                    if item is None:
                        continue
                    if not isinstance(item, expected_type):
                        raise TypeError(
                            f"Cannot cast object list to {expected_type.__name__} list (ClassCastException: [Ljava.lang.Object; cannot be cast to [Ljava.lang.{expected_type.__name__};)"
                        )
        if inferred_type is not object and inferred_type is not expected_type and expected_type is not object:
            if not issubclass(inferred_type, expected_type):
                raise TypeError(
                    f"Cannot cast {inferred_type.__name__} list to {expected_type.__name__} list"
                )
    return new_list