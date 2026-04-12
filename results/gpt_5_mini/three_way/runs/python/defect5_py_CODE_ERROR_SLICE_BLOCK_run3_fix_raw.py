@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is not None and len(array) > 0:
        inferred_type = type(array[0])
    elif element is not None:
        inferred_type = type(element)
    else:
        inferred_type = object

    new_list = ArrayUtils._copy_list_grow1(array, inferred_type)
    new_list[len(new_list) - 1] = element

    if expected_type is not None:
        # If we couldn't infer a concrete element type (object) but an expected_type
        # was provided, do not raise if element is None — allow None to be added to any typed list.
        if inferred_type == object and expected_type != object and element is not None:
            # If the inferred element type is not compatible with expected_type, raise
            if not issubclass(inferred_type, expected_type):
                raise TypeError(
                    f"Cannot cast list elements to {expected_type.__name__} list "
                    f"(ClassCastException: [Ljava.lang.{inferred_type.__name__}; cannot be cast to "
                    f"[Ljava.lang.{expected_type.__name__};)"
                )
    return new_list