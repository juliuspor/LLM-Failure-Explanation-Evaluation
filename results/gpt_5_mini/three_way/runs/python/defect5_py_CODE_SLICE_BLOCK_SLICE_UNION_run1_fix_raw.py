@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is not None:
        # infer element type from first non-None element if possible
        inferred_type = None
        for item in array:
            if item is not None:
                inferred_type = type(item)
                break
    elif element is not None:
        inferred_type = type(element)
    else:
        inferred_type = None

    new_list = ArrayUtils._copy_list_grow1(array, inferred_type)
    new_list[len(new_list) - 1] = element

    if expected_type is not None:
        # If we couldn't infer a specific element type (None) but an expected_type
        # is provided and it's not the generic 'object', simulate a cast failure.
        if inferred_type is None and expected_type is not object:
            raise TypeError(
                f"Cannot cast list elements to {expected_type.__name__} list"
            )

    return new_list