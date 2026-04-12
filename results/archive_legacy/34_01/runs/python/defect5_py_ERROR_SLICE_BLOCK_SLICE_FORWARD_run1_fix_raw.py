@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is not None:
        # infer element type from contents
        inferred_type = None
        for item in array:
            if item is not None:
                t = type(item)
                if inferred_type is None:
                    inferred_type = t
                elif inferred_type != t:
                    inferred_type = object
                    break
        if inferred_type is None:
            inferred_type = object
    elif element is not None:
        inferred_type = type(element)
    else:
        inferred_type = object

    new_list = ArrayUtils._copy_list_grow1(array, inferred_type)
    new_list[len(new_list) - 1] = element

    if expected_type is not None:
        if inferred_type == object and expected_type != object:
            # try to coerce elements to expected_type
            source = array if array is not None else []
            coerced = []
            try:
                for item in source:
                    if item is None:
                        coerced.append(None)
                    else:
                        coerced.append(expected_type(item))
                if element is None:
                    coerced.append(None)
                else:
                    coerced.append(expected_type(element))
            except Exception:
                raise TypeError(
                    f"Cannot cast object list to {expected_type.__name__} list "
                    f"(ClassCastException: [Ljava.lang.Object; cannot be cast to "
                    f"[Ljava.lang.{expected_type.__name__};)"
                )
            return coerced
    return new_list