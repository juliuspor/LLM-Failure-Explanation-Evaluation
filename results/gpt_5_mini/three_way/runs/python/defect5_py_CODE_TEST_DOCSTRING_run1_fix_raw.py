@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is not None:
        # determine component type from array contents if possible
        if len(array) > 0 and array[0] is not None:
            component_type = type(array[0])
        else:
            # if array is empty or first element is None, prefer expected_type if given
            if expected_type is not None:
                component_type = expected_type
            elif element is not None:
                component_type = type(element)
            else:
                component_type = object
    elif element is not None:
        component_type = type(element)
    elif expected_type is not None:
        component_type = expected_type
    else:
        component_type = object

    new_list = ArrayUtils._copy_list_grow1(array, component_type)
    new_list[len(new_list) - 1] = element

    # Only simulate a type error if expected_type is provided and element is not None
    # and the element is not an instance of expected_type. None is allowed.
    if expected_type is not None and element is not None:
        if not isinstance(element, expected_type):
            raise TypeError(
                f"Cannot cast element of type {type(element).__name__} to {expected_type.__name__}"
            )

    return new_list