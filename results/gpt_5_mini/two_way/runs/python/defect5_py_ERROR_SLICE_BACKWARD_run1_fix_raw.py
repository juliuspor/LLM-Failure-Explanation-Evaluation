@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is not None:
        # determine component type by inspecting elements for a non-None sample
        component_type = None
        for item in array:
            if item is not None:
                component_type = type(item)
                break
        if component_type is None:
            # array exists but all elements are None -> fall back to element type or object
            component_type = type(element) if element is not None else object
    elif element is not None:
        component_type = type(element)
    else:
        component_type = object

    # Create new list extended by one slot
    new_list: List[Any] = ArrayUtils._copy_list_grow1(array, component_type)
    new_list[len(new_list) - 1] = element

    # If expected_type is provided, ensure compatibility. If component_type is object but
    # expected_type is more specific, attempt to coerce existing elements and the new element
    # into expected_type. If coercion fails, raise TypeError to simulate ClassCastException.
    if expected_type is not None:
        def try_convert(value):
            if value is None:
                return None
            if isinstance(value, expected_type):
                return value
            try:
                return expected_type(value)
            except Exception:
                raise TypeError(
                    f"Cannot cast element of type {type(value).__name__} to {expected_type.__name__}"
                )

        # Attempt conversion for all elements
        converted = []
        for v in new_list:
            converted.append(try_convert(v))
        # return converted list with proper typing
        return converted  # type: ignore

    return new_list  # type: ignore