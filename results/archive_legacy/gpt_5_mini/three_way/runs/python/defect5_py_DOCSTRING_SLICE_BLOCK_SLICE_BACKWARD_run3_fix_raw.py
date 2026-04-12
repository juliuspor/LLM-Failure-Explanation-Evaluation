@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    inferred_type = None
    if array is not None and len(array) > 0:
        for itm in array:
            if itm is not None:
                inferred_type = type(itm)
                break
    if inferred_type is None and element is not None:
        inferred_type = type(element)
    if inferred_type is None:
        inferred_type = object
    new_list = ArrayUtils._copy_list_grow1(array, inferred_type)
    new_list[len(new_list) - 1] = element
    if expected_type is not None:
        if inferred_type is not object:
            try:
                if not issubclass(inferred_type, expected_type):
                    raise TypeError(f"Cannot cast {inferred_type.__name__} list to {expected_type.__name__} list (ClassCastException: [Ljava.lang.{inferred_type.__name__}; cannot be cast to [Ljava.lang.{expected_type.__name__};)")
            except TypeError:
                raise
            except Exception:
                pass
    return new_list