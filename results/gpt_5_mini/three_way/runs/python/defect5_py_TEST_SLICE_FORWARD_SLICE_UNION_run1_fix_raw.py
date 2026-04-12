@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is not None and len(array) > 0:
        # infer from first element of the array
        first = array[0]
        inferred_type = type(first) if first is not None else object
    elif element is not None:
        inferred_type = type(element)
    elif expected_type is not None:
        inferred_type = expected_type
    else:
        inferred_type = object

    new_list = ArrayUtils._copy_list_grow1(array, inferred_type)
    new_list[len(new_list) - 1] = element

    if expected_type is not None:
        # If we only know object but an expected_type was requested, accept it
        if inferred_type is object:
            inferred_type = expected_type
        # If we have a more specific inferred_type, ensure it's compatible with expected_type
        else:
            try:
                if not issubclass(inferred_type, expected_type):
                    raise TypeError(
                        f"Cannot cast {inferred_type.__name__} list to {expected_type.__name__} list "
                        f"(ClassCastException: [Ljava.lang.{inferred_type.__name__}; cannot be cast to "
                        f"[Ljava.lang.{expected_type.__name__};)"
                    )
            except TypeError:
                # if inferred_type is not a class (e.g., typing constructs), skip issubclass check
                pass

    return new_list