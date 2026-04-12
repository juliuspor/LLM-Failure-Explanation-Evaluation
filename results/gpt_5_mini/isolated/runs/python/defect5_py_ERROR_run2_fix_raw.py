@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is not None:
        # infer element type from existing array contents (first non-None element)
        inferred_element_type = object
        for itm in array:
            if itm is not None:
                inferred_element_type = type(itm)
                break
    elif element is not None:
        inferred_element_type = type(element)
    else:
        inferred_element_type = object

    new_list = ArrayUtils._copy_list_grow1(array, inferred_element_type)
    new_list[len(new_list) - 1] = element

    if expected_type is not None:
        # Simulate Java-style cast failure: if we only know element type as object
        # but expected_type is more specific, raise TypeError
        if inferred_element_type is object and expected_type is not object:
            raise TypeError(
                f"Cannot cast object list to {expected_type.__name__} list "
                f"(ClassCastException: [Ljava.lang.Object; cannot be cast to "
                f"[Ljava.lang.{expected_type.__name__};)"
            )
    return new_list