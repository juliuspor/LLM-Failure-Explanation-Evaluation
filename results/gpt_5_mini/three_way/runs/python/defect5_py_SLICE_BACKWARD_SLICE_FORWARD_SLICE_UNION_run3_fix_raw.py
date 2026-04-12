@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is not None:
        # infer element type by looking for first non-None element
        inferred_elem_type = None
        for item in array:
            if item is not None:
                inferred_elem_type = type(item)
                break
        if inferred_elem_type is None and element is not None:
            inferred_elem_type = type(element)
        if inferred_elem_type is None:
            inferred_elem_type = object
    elif element is not None:
        inferred_elem_type = type(element)
    else:
        inferred_elem_type = object

    new_list = ArrayUtils._copy_list_grow1(array, inferred_elem_type)
    new_list[len(new_list) - 1] = element

    if expected_type is not None:
        # If we don't know element type (object) but expected_type is specific, consider element compatibility
        if inferred_elem_type is object:
            # If element provided, check it against expected_type
            if element is not None and not isinstance(element, expected_type):
                raise TypeError(
                    f"Cannot cast object list to {expected_type.__name__} list "
                    f"(ClassCastException: [Ljava.lang.Object; cannot be cast to "
                    f"[Ljava.lang.{expected_type.__name__};)"
                )
            # otherwise unknown but no concrete mismatch, allow
        else:
            # If inferred element type is known, ensure it's compatible with expected_type
            try:
                if not issubclass(inferred_elem_type, expected_type):
                    # If element itself incompatible, raise
                    if element is None or not isinstance(element, expected_type):
                        raise TypeError(
                            f"Cannot cast {inferred_elem_type.__name__} list to {expected_type.__name__} list "
                            f"(ClassCastException: [Ljava.lang.{inferred_elem_type.__name__}; cannot be cast to "
                            f"[Ljava.lang.{expected_type.__name__};)"
                        )
            except TypeError:
                # issubclass can raise TypeError if expected_type is not a class; in that case, fall back to isinstance checks
                if element is not None and not isinstance(element, expected_type):
                    raise TypeError(
                        f"Cannot cast object list to {expected_type.__name__} list "
                        f"(ClassCastException: [Ljava.lang.Object; cannot be cast to "
                        f"[Ljava.lang.{expected_type.__name__};)"
                    )

    return new_list