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
                if element is not None:
                    inferred_type = type(element)
                elif expected_type is not None:
                    inferred_type = expected_type
                else:
                    inferred_type = object
        else:
            if element is not None:
                inferred_type = type(element)
            elif expected_type is not None:
                inferred_type = expected_type
            else:
                inferred_type = object
    elif element is not None:
        inferred_type = type(element)
    elif expected_type is not None:
        inferred_type = expected_type
    else:
        inferred_type = object

    new_list = ArrayUtils._copy_list_grow1(array, inferred_type)
    new_list[len(new_list) - 1] = element

    if expected_type is not None:
        if inferred_type == object:
            if array is not None and len(array) > 0:
                for itm in array:
                    if itm is not None and not isinstance(itm, expected_type):
                        raise TypeError(
                            f"Cannot cast object list to {expected_type.__name__} list "
                            f"(ClassCastException: [Ljava.lang.Object; cannot be cast to "
                            f"[Ljava.lang.{expected_type.__name__};)"
                        )
                if element is not None and not isinstance(element, expected_type):
                    raise TypeError(
                        f"Cannot cast object list to {expected_type.__name__} list "
                        f"(ClassCastException: [Ljava.lang.Object; cannot be cast to "
                        f"[Ljava.lang.{expected_type.__name__};)"
                    )
            else:
                if element is not None and not isinstance(element, expected_type):
                    raise TypeError(
                        f"Cannot cast object list to {expected_type.__name__} list "
                        f"(ClassCastException: [Ljava.lang.Object; cannot be cast to "
                        f"[Ljava.lang.{expected_type.__name__};)"
                    )
        elif inferred_type != expected_type:
            if not issubclass(inferred_type, expected_type):
                raise TypeError(
                    f"Cannot cast {inferred_type.__name__} list to {expected_type.__name__} list "
                    f"(ClassCastException: [Ljava.lang.{inferred_type.__name__}; cannot be cast to "
                    f"[Ljava.lang.{expected_type.__name__};)"
                )

    return new_list