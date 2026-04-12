@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is not None and len(array) > 0:
        # Infer component type from first element
        first_elem = array[0]
        inferred_type = type(first_elem) if first_elem is not None else object
    elif element is not None:
        inferred_type = type(element)
    else:
        inferred_type = object

    new_list = ArrayUtils._copy_list_grow1(array, inferred_type)
    new_list[len(new_list) - 1] = element

    if expected_type is not None:
        # If expected_type provided, ensure the element is instance of it (or None allowed)
        if element is not None and not isinstance(element, expected_type):
            raise TypeError(
                f"Cannot add element of type {type(element).__name__} to list of expected element type {expected_type.__name__}"
            )

    return new_list