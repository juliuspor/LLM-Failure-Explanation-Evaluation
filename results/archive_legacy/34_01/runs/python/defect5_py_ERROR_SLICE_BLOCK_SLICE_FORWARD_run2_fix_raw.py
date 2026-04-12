@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is not None:
        non_none = [x for x in array if x is not None]
        if non_none:
            first_type = type(non_none[0])
            if all(isinstance(x, first_type) for x in non_none):
                inferred_type = first_type
            else:
                inferred_type = object
        else:
            inferred_type = object
    elif element is not None:
        inferred_type = type(element)
    else:
        inferred_type = object

    new_list = ArrayUtils._copy_list_grow1(array, inferred_type)
    new_list[len(new_list) - 1] = element

    if expected_type is not None:
        if expected_type != object:
            if inferred_type == object:
                all_ok = True
                source = [] if array is None else array
                for x in source:
                    if x is not None and not isinstance(x, expected_type):
                        all_ok = False
                        break
                if element is not None and not isinstance(element, expected_type):
                    all_ok = False
                if not all_ok:
                    raise TypeError(
                        f"Cannot cast object list to {expected_type.__name__} list "
                        f"(ClassCastException: [Ljava.lang.Object; cannot be cast to "
                        f"[Ljava.lang.{expected_type.__name__};)"
                    )
            else:
                if not issubclass(inferred_type, expected_type):
                    raise TypeError(
                        f"Cannot cast {inferred_type.__name__} list to {expected_type.__name__} list"
                    )
    return new_list