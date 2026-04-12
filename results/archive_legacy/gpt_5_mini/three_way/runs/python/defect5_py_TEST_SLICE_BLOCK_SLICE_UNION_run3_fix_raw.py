@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is not None:
        inferred_type = None
        for v in array:
            if v is not None:
                inferred_type = type(v)
                break
        if inferred_type is None:
            inferred_type = expected_type if expected_type is not None else object
    elif element is not None:
        inferred_type = type(element)
    else:
        inferred_type = expected_type if expected_type is not None else object

    new_list = ArrayUtils._copy_list_grow1(array, inferred_type)
    new_list[len(new_list) - 1] = element

    if expected_type is not None:
        if inferred_type == object:
            inferred_type = expected_type
        elif expected_type != object:
            try:
                if not issubclass(inferred_type, expected_type):
                    raise TypeError(
                        f"Cannot cast {inferred_type.__name__} list to {expected_type.__name__} list "
                        f"(ClassCastException: [Ljava.lang.{inferred_type.__name__}; cannot be cast to "
                        f"[Ljava.lang.{expected_type.__name__};)"
                    )
            except TypeError:
                raise
            except Exception:
                pass

    return new_list