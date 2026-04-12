@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is not None:
        inferred_type = type(array)
    elif element is not None:
        inferred_type = type(element)
    elif expected_type is not None:
        inferred_type = expected_type
    else:
        inferred_type = object

    new_list = ArrayUtils._copy_list_grow1(array, inferred_type)
    new_list[len(new_list) - 1] = element

    if expected_type is not None:
        # If inferred_type is the generic object (no information) but caller expects a specific type,
        # simulate Java-like ClassCastException by raising TypeError.
        if inferred_type == object and expected_type != object:
            raise TypeError(
                f"Cannot cast object list to {expected_type.__name__} list "
                f"(ClassCastException: [Ljava.lang.Object; cannot be cast to "
                f"[Ljava.lang.{expected_type.__name__};)"
            )
        # If inferred_type is a type object (e.g., element's or expected_type), ensure compatibility
        # If inferred_type is a list type, compare component types; otherwise, if inferred_type is
        # not expected_type and neither is object, raise TypeError to reflect incompatible types.
        if inferred_type is not object and inferred_type is not expected_type:
            # For Python lists, type(array) will be 'list' so this branch is mostly for when
            # inferred_type was set from expected_type above or element type differs explicitly.
            # We only raise when there's a clear mismatch between element type and expected_type
            # For element being not None, ensure element is instance of expected_type
            if element is not None and not isinstance(element, expected_type):
                raise TypeError(
                    f"Element of type {type(element).__name__} cannot be added to list of {expected_type.__name__}"
                )
    return new_list