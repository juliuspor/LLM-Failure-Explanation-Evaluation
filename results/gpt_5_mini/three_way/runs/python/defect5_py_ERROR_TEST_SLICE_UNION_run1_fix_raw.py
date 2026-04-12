@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if expected_type is not None:
        inferred_type = expected_type
    else:
        # Derive element type from array contents if possible
        if array is not None and len(array) > 0:
            inferred_type = object
            for item in array:
                if item is not None:
                    inferred_type = type(item)
                    break
            else:
                # all elements are None
                if element is not None:
                    inferred_type = type(element)
                else:
                    inferred_type = object
        elif element is not None:
            inferred_type = type(element)
        else:
            inferred_type = object

    new_list = ArrayUtils._copy_list_grow1(array, inferred_type)
    new_list[len(new_list) - 1] = element

    # If expected_type was provided, ensure compatibility with known inferred_type
    if expected_type is not None:
        # If inferred_type is not object and not subclass of expected_type, raise
        if inferred_type is not object and not issubclass(inferred_type, expected_type):
            raise TypeError(
                f"Cannot cast {inferred_type.__name__} list to {expected_type.__name__} list "
                f"(ClassCastException: [Ljava.lang.{inferred_type.__name__}; cannot be cast to "
                f"[Ljava.lang.{expected_type.__name__};)"
            )

    return new_list