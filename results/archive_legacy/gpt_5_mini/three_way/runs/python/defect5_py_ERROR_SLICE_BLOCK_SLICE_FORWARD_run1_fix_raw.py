@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is not None:
        inferred_type = type(array)
    elif element is not None:
        inferred_type = type(element)
    else:
        inferred_type = object

    if array is None:
        new_list = ArrayUtils._copy_list_grow1(array, inferred_type)
        new_list[len(new_list) - 1] = element
        if expected_type is not None and element is not None and not isinstance(element, expected_type):
            try:
                new_list[len(new_list) - 1] = expected_type(element)
            except Exception:
                raise TypeError(f"Cannot cast element of type {type(element).__name__} to {expected_type.__name__}")
        return new_list

    if expected_type is not None:
        coerced = []
        for idx, itm in enumerate(array):
            if itm is None:
                coerced.append(None)
                continue
            if isinstance(itm, expected_type):
                coerced.append(itm)
            else:
                try:
                    coerced.append(expected_type(itm))
                except Exception:
                    raise TypeError(f"Cannot cast element at index {idx} of type {type(itm).__name__} to {expected_type.__name__}")
        new_list = coerced.copy()
        new_list.append(None)
        new_list[len(new_list) - 1] = element if (element is None or isinstance(element, expected_type)) else _try_cast(element, expected_type)
        return new_list

    new_list = ArrayUtils._copy_list_grow1(array, inferred_type)
    new_list[len(new_list) - 1] = element
    return new_list


def _try_cast(value, typ):
    try:
        return typ(value)
    except Exception:
        raise TypeError(f"Cannot cast element of type {type(value).__name__} to {typ.__name__}")