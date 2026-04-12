@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is not None:
        # Infer element type from existing non-None elements in the list
        inferred_element_type = object
        for item in array:
            if item is not None:
                inferred_element_type = type(item)
                break
        # If all elements are None and element is not None, use element's type
        if inferred_element_type is object and element is not None:
            inferred_element_type = type(element)
    elif element is not None:
        inferred_element_type = type(element)
    else:
        inferred_element_type = object

    new_list = ArrayUtils._copy_list_grow1(array, inferred_element_type)
    new_list[len(new_list) - 1] = element

    if expected_type is not None:
        # If we couldn't infer a concrete element type (object) but an expected_type
        # is provided and differs, simulate a cast failure.
        if inferred_element_type is object and expected_type is not object:
            raise TypeError(
                f"Cannot cast list elements to {expected_type.__name__}: incompatible types"
            )
    return new_list