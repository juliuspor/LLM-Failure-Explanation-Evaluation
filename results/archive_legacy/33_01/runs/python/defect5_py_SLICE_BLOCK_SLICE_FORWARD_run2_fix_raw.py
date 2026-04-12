@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is not None:
        if len(array) == 0 and expected_type is not None:
            inferred_type = expected_type
        else:
            inferred_type = type(array[0]) if len(array) > 0 else object
            for item in array:
                if item is not None and inferred_type is not object and type(item) != inferred_type:
                    inferred_type = object
                    break
    elif element is not None:
        inferred_type = type(element)
    else:
        inferred_type = object

    new_list = ArrayUtils._copy_list_grow1(array, inferred_type)
    new_list[len(new_list) - 1] = element

    if expected_type is not None:
        if inferred_type == object:
            elements_to_check = [] if new_list is None else new_list
            for e in elements_to_check:
                if e is None:
                    continue
                if not isinstance(e, expected_type):
                    raise TypeError(
                        f"Cannot cast object list to {expected_type.__name__} list "
                        f"(ClassCastException: [Ljava.lang.Object; cannot be cast to "
                        f"[Ljava.lang.{expected_type.__name__};)"
                    )
        else:
            if inferred_type != expected_type and inferred_type is not object:
                raise TypeError(
                    f"Cannot cast {inferred_type.__name__} list to {expected_type.__name__} list "
                    f"(ClassCastException: [Ljava.lang.{inferred_type.__name__}; cannot be cast to "
                    f"[Ljava.lang.{expected_type.__name__};)"
                )

    return new_list