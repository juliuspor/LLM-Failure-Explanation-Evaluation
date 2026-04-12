@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is None:
        inferred_element_type = type(element) if element is not None else object
    else:
        # Try to infer element type from existing elements
        inferred_element_type = object
        for item in array:
            if item is not None:
                inferred_element_type = type(item)
                break
        # If array had only None values and element is not None, use element's type
        if inferred_element_type is object and element is not None:
            inferred_element_type = type(element)

    new_list = ArrayUtils._copy_list_grow1(array, inferred_element_type)
    new_list[len(new_list) - 1] = element

    if expected_type is not None:
        # If we couldn't determine a concrete element type (object) but expected_type is more specific, simulate cast failure
        if inferred_element_type is object and expected_type != object:
            raise TypeError(
                f"Cannot cast object list to {expected_type.__name__} list "
                f"(ClassCastException: [Ljava.lang.Object; cannot be cast to "
                f"[Ljava.lang.{expected_type.__name__};)"
            )
        # If array existed, ensure existing non-None elements are compatible with expected_type
        if array is not None:
            for item in array:
                if item is not None and not isinstance(item, expected_type):
                    raise TypeError(
                        f"Cannot cast list elements to {expected_type.__name__}"
                    )
        # Also ensure the new element is compatible
        if element is not None and not isinstance(element, expected_type):
            raise TypeError(
                f"Cannot add element of type {type(element).__name__} to {expected_type.__name__} list"
            )

    return new_list