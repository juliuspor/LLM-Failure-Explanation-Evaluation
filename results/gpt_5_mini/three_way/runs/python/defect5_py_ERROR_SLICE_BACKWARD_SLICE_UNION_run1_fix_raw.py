@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is not None:
        # infer element type from first non-None element in array
        inferred_type = object
        for item in array:
            if item is not None:
                inferred_type = type(item)
                break
    elif element is not None:
        inferred_type = type(element)
    else:
        inferred_type = object

    new_list = ArrayUtils._copy_list_grow1(array, inferred_type)
    new_list[len(new_list) - 1] = element

    if expected_type is not None:
        # If we couldn't infer a specific type, try to validate/cast elements to expected_type
        if inferred_type == object and expected_type != object:
            # verify all existing elements (except the appended one which we also check) are instances of expected_type or None
            for i, itm in enumerate(new_list):
                if itm is None:
                    continue
                if not isinstance(itm, expected_type):
                    raise TypeError(
                        f"Cannot cast list elements to {expected_type.__name__}: element at index {i} is {type(itm).__name__}"
                    )
    return new_list