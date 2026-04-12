@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is None:
        # If array is None, simply return a new list with the element
        new_list: List[T] = []
        new_list.append(element)
        inferred_element_type = type(element) if element is not None else object
    else:
        # When array is present, infer element type from an existing element if possible
        inferred_element_type = object
        for item in array:
            if item is not None:
                inferred_element_type = type(item)
                break
        # Make a shallow copy and append the new element
        new_list = array.copy()
        new_list.append(element)

    # Simulate Java-style ClassCastException behavior when expected_type provided
    if expected_type is not None:
        if inferred_element_type == object and expected_type != object:
            raise TypeError(
                f"Cannot cast object list to {expected_type.__name__} list "
                f"(ClassCastException: [Ljava.lang.Object; cannot be cast to "
                f"[Ljava.lang.{expected_type.__name__};)"
            )
    return new_list