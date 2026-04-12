@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is not None:
        # Try to infer element component type from existing elements if possible
        if len(array) > 0:
            # Use the type of the first non-None element if available
            inferred_elem_type = None
            for it in array:
                if it is not None:
                    inferred_elem_type = type(it)
                    break
            if inferred_elem_type is None:
                inferred_elem_type = object
        else:
            # Empty array: component type is unknown; treat as object
            inferred_elem_type = object
    elif element is not None:
        inferred_elem_type = type(element)
    else:
        inferred_elem_type = object

    new_list = ArrayUtils._copy_list_grow1(array, inferred_elem_type)
    new_list[len(new_list) - 1] = element

    # Only simulate a ClassCastException if we have an actual existing array whose
    # element types are more general than the expected_type. If array was None,
    # we are creating a new list and should not fail the cast.
    if expected_type is not None and array is not None:
        if inferred_elem_type == object and expected_type != object:
            raise TypeError(
                f"Cannot cast object list to {expected_type.__name__} list "
                f"(ClassCastException: [Ljava.lang.Object; cannot be cast to "
                f"[Ljava.lang.{expected_type.__name__};)"
            )

    return new_list