@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is not None:
        # infer element type from existing elements: find first non-None element
        inferred_elem_type = None
        for itm in array:
            if itm is not None:
                inferred_elem_type = type(itm)
                break
        if inferred_elem_type is None:
            # all elements are None or array empty -> treat as unknown
            inferred_elem_type = object
    elif element is not None:
        inferred_elem_type = type(element)
    else:
        inferred_elem_type = object

    new_list = ArrayUtils._copy_list_grow1(array, inferred_elem_type)
    new_list[len(new_list) - 1] = element

    if expected_type is not None:
        # If we have a concrete inferred element type, ensure compatibility
        if inferred_elem_type is not object and not issubclass(inferred_elem_type, expected_type):
            raise TypeError(
                f"Cannot cast {inferred_elem_type.__name__} list to {expected_type.__name__} list "
                f"(ClassCastException: [Ljava.lang.{inferred_elem_type.__name__}; cannot be cast to "
                f"[Ljava.lang.{expected_type.__name__};)"
            )
        # If inferred is object but element itself conflicts with expected_type, check element
        if inferred_elem_type is object and element is not None and not isinstance(element, expected_type):
            raise TypeError(
                f"Cannot cast object list to {expected_type.__name__} list "
                f"(ClassCastException: [Ljava.lang.Object; cannot be cast to "
                f"[Ljava.lang.{expected_type.__name__};)"
            )

    return new_list