@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is not None:
        inferred_type = None
        for x in array:
            if x is not None:
                inferred_type = type(x)
                break
    elif element is not None:
        inferred_type = type(element)
    else:
        inferred_type = None

    if inferred_type is None and expected_type is not None:
        inferred_type = expected_type
    if inferred_type is None:
        inferred_type = object

    new_list = ArrayUtils._copy_list_grow1(array, inferred_type)
    new_list[len(new_list) - 1] = element

    if expected_type is not None and inferred_type is not object:
        try:
            if not issubclass(inferred_type, expected_type) and not issubclass(expected_type, inferred_type):
                raise TypeError(
                    f"Cannot cast object list to {expected_type.__name__} list "
                    f"(ClassCastException: [Ljava.lang.Object; cannot be cast to "
                    f"[Ljava.lang.{expected_type.__name__};)"
                )
        except TypeError:
            raise
        except Exception:
            pass

    return new_list