@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is not None and len(array) > 0:
        inferred_element_type = type(array[0])
    elif element is not None:
        inferred_element_type = type(element)
    else:
        inferred_element_type = object

    new_list = ArrayUtils._copy_list_grow1(array, inferred_element_type)
    new_list[len(new_list) - 1] = element

    if expected_type is not None:
        # If we only know the container element type is 'object' (unknown) but expected_type is more specific, fail
        if inferred_element_type is object and expected_type is not object:
            raise TypeError(
                f"Cannot cast object list to {expected_type.__name__} list "
                f"(ClassCastException: [Ljava.lang.Object; cannot be cast to "
                f"[Ljava.lang.{expected_type.__name__};)"
            )
        # If we have a concrete inferred element type, ensure it's compatible with expected_type
        try:
            # issubclass requires types; handle instances by taking the type
            if not issubclass(inferred_element_type, expected_type):
                raise TypeError(
                    f"Cannot cast {inferred_element_type.__name__} list to {expected_type.__name__} list "
                    f"(ClassCastException: [Ljava.lang.{inferred_element_type.__name__}; cannot be cast to "
                    f"[Ljava.lang.{expected_type.__name__};)"
                )
        except TypeError:
            # issubclass can raise TypeError if expected_type is not a class; in that case, skip strict check
            pass

    return new_list