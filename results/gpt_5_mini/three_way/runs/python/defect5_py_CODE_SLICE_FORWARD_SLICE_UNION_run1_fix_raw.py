@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is not None and len(array) > 0:
        # infer element type from existing elements
        inferred_element_type = type(array[0])
    elif element is not None:
        inferred_element_type = type(element)
    else:
        inferred_element_type = None

    # If expected_type is provided, perform a Pythonic type check on the element
    if expected_type is not None and element is not None and not isinstance(element, expected_type):
        raise TypeError(
            f"Cannot add element of type {type(element).__name__} to list expected to hold {expected_type.__name__}"
        )

    new_list = ArrayUtils._copy_list_grow1(array, inferred_element_type)
    new_list[len(new_list) - 1] = element

    return new_list