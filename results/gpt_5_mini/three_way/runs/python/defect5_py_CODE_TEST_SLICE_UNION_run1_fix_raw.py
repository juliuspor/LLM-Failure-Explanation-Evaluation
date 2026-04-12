@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is not None and len(array) > 0:
        # Infer type from first non-None element in the array if possible
        inferred_element_type = None
        for itm in array:
            if itm is not None:
                inferred_element_type = type(itm)
                break
        if inferred_element_type is None:
            # all elements are None; prefer expected_type if provided
            inferred_element_type = expected_type if expected_type is not None else object
    elif element is not None:
        inferred_element_type = type(element)
    else:
        # array is None or empty and element is None
        inferred_element_type = expected_type if expected_type is not None else object

    # If expected_type provided, ensure compatibility
    if expected_type is not None:
        # If we only know object (unknown), but expected_type is specific, simulate ClassCastException
        if inferred_element_type is object and expected_type is not object:
            raise TypeError(
                f"Cannot cast object list to {expected_type.__name__} list "
                f"(ClassCastException: [Ljava.lang.Object; cannot be cast to "
                f"[Ljava.lang.{expected_type.__name__};)"
            )
        # If inferred_element_type is concrete and not subclass of expected_type, raise
        try:
            if inferred_element_type is not object and not issubclass(inferred_element_type, expected_type):
                raise TypeError(
                    f"Cannot cast {inferred_element_type.__name__} list to {expected_type.__name__} list"
                )
        except TypeError:
            # issubclass may raise if inferred_element_type is not a class
            pass

    new_list = ArrayUtils._copy_list_grow1(array, inferred_element_type)
    new_list[len(new_list) - 1] = element
    return new_list