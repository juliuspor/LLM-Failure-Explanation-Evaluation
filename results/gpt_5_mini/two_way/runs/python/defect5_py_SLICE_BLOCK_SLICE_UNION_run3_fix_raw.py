@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is not None:
        inferred_type = type(array)
    elif element is not None:
        inferred_type = type(element)
    else:
        inferred_type = object

    new_list = ArrayUtils._copy_list_grow1(array, inferred_type)
    new_list[len(new_list) - 1] = element

    if expected_type is not None:
        # If we couldn't infer a concrete element/container type (object),
        # validate each element can be considered an instance of expected_type
        # before allowing the operation. None elements are acceptable.
        if inferred_type == object:
            # Check existing elements (from array) and the new element
            if array is not None:
                for i, val in enumerate(array):
                    if val is not None and not isinstance(val, expected_type):
                        raise TypeError(
                            f"Element at index {i} with value {val!r} is not of type {expected_type.__name__}"
                        )
            # Check the appended element (it's at the end)
            if element is not None and not isinstance(element, expected_type):
                raise TypeError(
                    f"Element to add with value {element!r} is not of type {expected_type.__name__}"
                )
        else:
            # If inferred_type is not object, ensure it's compatible with expected_type
            # For container types, we compare element types where possible.
            # If array is a list subclass, we still validate items.
            if array is not None:
                for i, val in enumerate(array):
                    if val is not None and not isinstance(val, expected_type):
                        raise TypeError(
                            f"Element at index {i} with value {val!r} is not of type {expected_type.__name__}"
                        )
            if element is not None and not isinstance(element, expected_type):
                raise TypeError(
                    f"Element to add with value {element!r} is not of type {expected_type.__name__}"
                )

    return new_list