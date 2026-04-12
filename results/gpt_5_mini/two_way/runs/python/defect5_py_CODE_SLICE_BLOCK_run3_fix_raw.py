@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if element is not None:
        inferred_type = type(element)
    else:
        # Try to infer from array contents: first non-None element's type
        inferred_type = object
        if array is not None:
            for item in array:
                if item is not None:
                    inferred_type = type(item)
                    break

    new_list = ArrayUtils._copy_list_grow1(array, inferred_type)
    new_list[len(new_list) - 1] = element

    if expected_type is not None:
        # If we couldn't infer a specific element type (object) but expected_type is specific, simulate cast failure
        if inferred_type is object and expected_type is not object:
            raise TypeError(
                f"Cannot cast object list to {expected_type.__name__} list "
                f"(ClassCastException: [Ljava.lang.Object; cannot be cast to "
                f"[Ljava.lang.{expected_type.__name__};)"
            )
    return new_list