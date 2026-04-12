@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is not None and len(array) > 0:
        # infer element type from first non-None element in the array
        inferred_elem_type = None
        for item in array:
            if item is not None:
                inferred_elem_type = type(item)
                break
        if inferred_elem_type is None:
            # all elements are None
            if element is not None:
                inferred_elem_type = type(element)
            else:
                inferred_elem_type = object
    elif element is not None:
        inferred_elem_type = type(element)
    else:
        inferred_elem_type = object

    new_list = ArrayUtils._copy_list_grow1(array, inferred_elem_type)
    new_list[len(new_list) - 1] = element

    if expected_type is not None:
        # simulate a type cast failure: if we couldn't infer a specific element type
        # (it's object) but an expected more specific type was requested, raise
        if inferred_elem_type == object and expected_type != object:
            raise TypeError(
                f"Cannot cast object list to {expected_type.__name__} list "
                f"(ClassCastException: [Ljava.lang.Object; cannot be cast to "
                f"[Ljava.lang.{expected_type.__name__};)"
            )

    return new_list