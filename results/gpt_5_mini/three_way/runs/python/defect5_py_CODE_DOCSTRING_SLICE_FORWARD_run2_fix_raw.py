@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is not None and len(array) > 0:
        # Try to infer component type from first non-None element in the array
        inferred_component_type = None
        for item in array:
            if item is not None:
                inferred_component_type = type(item)
                break
        if inferred_component_type is None:
            # all elements are None
            inferred_component_type = type(element) if element is not None else object
    else:
        inferred_component_type = type(element) if element is not None else object

    # Build a new list that is a copy of the original (or empty) and append a placeholder
    new_list: List[Any] = array.copy() if array is not None else []
    new_list.append(None)

    # Set the last element to the provided element
    new_list[-1] = element

    # Simulate Java-style component type checking when expected_type is provided
    if expected_type is not None:
        # If we couldn't infer a more specific component type (object) but an expected_type was given,
        # raise a TypeError to mirror a ClassCastException scenario.
        if inferred_component_type is object and expected_type is not object:
            raise TypeError(
                f"Cannot cast object list to {expected_type.__name__} list "
                f"(ClassCastException: [Ljava.lang.Object; cannot be cast to "
                f"[Ljava.lang.{expected_type.__name__};)"
            )

    return new_list