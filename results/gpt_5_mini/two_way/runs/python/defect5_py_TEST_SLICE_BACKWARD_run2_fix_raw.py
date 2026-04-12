@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is not None:
        # If array has any non-None element, infer from that element's type
        inferred_type = object
        for item in array:
            if item is not None:
                inferred_type = type(item)
                break
        else:
            # all elements are None
            inferred_type = expected_type if expected_type is not None else object
    elif element is not None:
        inferred_type = type(element)
    else:
        # both array and element are None
        inferred_type = expected_type if expected_type is not None else object

    new_list = ArrayUtils._copy_list_grow1(array, inferred_type)
    new_list[len(new_list) - 1] = element

    # Do not raise TypeError; if expected_type is provided, we accept creating a list
    # whose intended element type is expected_type. This mirrors Java behavior of
    # creating an array of the requested component type when possible.
    return new_list