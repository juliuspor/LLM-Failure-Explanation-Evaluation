@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is not None:
        if len(array) > 0:
            inferred_type = None
            for itm in array:
                if itm is not None:
                    inferred_type = type(itm)
                    break
            if inferred_type is None:
                if expected_type is not None:
                    inferred_type = expected_type
                elif element is not None:
                    inferred_type = type(element)
                else:
                    inferred_type = object
        else:
            if expected_type is not None:
                inferred_type = expected_type
            elif element is not None:
                inferred_type = type(element)
            else:
                inferred_type = object
    elif element is not None:
        inferred_type = type(element)
    elif expected_type is not None:
        inferred_type = expected_type
    else:
        inferred_type = object

    if expected_type is not None:
        if inferred_type == object:
            inferred_type = expected_type
        else:
            try:
                if not issubclass(inferred_type, expected_type):
                    raise TypeError(
                        f"Cannot cast {inferred_type.__name__} list to {expected_type.__name__} list"
                    )
            except TypeError:
                raise
            except Exception:
                pass

    new_list = ArrayUtils._copy_list_grow1(array, inferred_type)
    new_list[len(new_list) - 1] = element
    return new_list