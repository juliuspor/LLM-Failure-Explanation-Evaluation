@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is not None:
        inferred_type = type(array)
    elif expected_type is not None:
        inferred_type = expected_type
    elif element is not None:
        inferred_type = type(element)
    else:
        inferred_type = object

    if expected_type is not None and element is not None:
        try:
            if not isinstance(element, expected_type):
                raise TypeError(
                    f"element of type {type(element).__name__} is not compatible with expected type {expected_type.__name__}"
                )
        except TypeError:
            raise
        except Exception:
            pass

    new_list = ArrayUtils._copy_list_grow1(array, inferred_type)
    new_list[len(new_list) - 1] = element

    if expected_type is not None:
        if inferred_type == object and expected_type != object:
            raise TypeError(
                f"Cannot cast object list to {expected_type.__name__} list "
                f"(ClassCastException: [Ljava.lang.Object; cannot be cast to "
                f"[Ljava.lang.{expected_type.__name__};)"
            )

    return new_list