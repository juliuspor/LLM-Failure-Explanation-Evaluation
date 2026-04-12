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

    if expected_type is not None and inferred_type == object and expected_type != object:
        try:
            if array is not None:
                coerced = []
                for i, item in enumerate(array):
                    if item is None:
                        coerced.append(None)
                    elif isinstance(item, expected_type):
                        coerced.append(item)
                    else:
                        coerced.append(expected_type(item))
                new_list = coerced
            else:
                new_list = []
        except Exception:
            raise TypeError(f"Cannot cast object list to {expected_type.__name__} list (ClassCastException: [Ljava.lang.Object; cannot be cast to [Ljava.lang.{expected_type.__name__};)")
        new_list.append(element)
        return new_list

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