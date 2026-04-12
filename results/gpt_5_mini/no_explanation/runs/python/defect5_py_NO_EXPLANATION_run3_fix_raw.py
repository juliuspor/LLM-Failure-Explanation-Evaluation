@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is not None:
        # try to infer element/component type from existing array contents
        inferred_element_type = None
        for item in array:
            if item is not None:
                inferred_element_type = type(item)
                break
        if inferred_element_type is None:
            # fallback to object if all elements are None
            inferred_element_type = object
    elif element is not None:
        inferred_element_type = type(element)
    else:
        inferred_element_type = object

    new_list = ArrayUtils._copy_list_grow1(array, inferred_element_type)
    new_list[len(new_list) - 1] = element

    if expected_type is not None:
        # if inferred element type is object (unknown) but expected_type is specific, simulate cast failure
        if inferred_element_type == object and expected_type != object:
            raise TypeError(
                f"Cannot cast object list to {expected_type.__name__} list "
                f"(ClassCastException: [Ljava.lang.Object; cannot be cast to "
                f"[Ljava.lang.{expected_type.__name__};)"
            )
        # if we have a concrete inferred type and element is not None, check compatibility
        if element is not None and not issubclass(inferred_element_type, expected_type):
            # Allow subclasses of expected_type; otherwise raise
            raise TypeError(
                f"Cannot add element of type {inferred_element_type.__name__} to list of {expected_type.__name__}"
            )

    return new_list