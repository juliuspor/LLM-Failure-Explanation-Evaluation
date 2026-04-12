@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if expected_type is not None:
        inferred_element_type = expected_type
    else:
        # Infer from array contents if possible
        inferred_element_type = object
        if array is not None:
            # look for first non-None element to infer type
            for item in array:
                if item is not None:
                    inferred_element_type = type(item)
                    break
        if inferred_element_type is object and element is not None:
            inferred_element_type = type(element)

    new_list = ArrayUtils._copy_list_grow1(array, inferred_element_type)
    new_list[len(new_list) - 1] = element

    if expected_type is not None:
        # simulate Java-style ClassCastException: only raise when inferred is object
        if inferred_element_type == object and expected_type != object:
            raise TypeError(
                f"Cannot cast object list to {expected_type.__name__} list "
                f"(ClassCastException: [Ljava.lang.Object; cannot be cast to "
                f"[Ljava.lang.{expected_type.__name__};)"
            )
    return new_list