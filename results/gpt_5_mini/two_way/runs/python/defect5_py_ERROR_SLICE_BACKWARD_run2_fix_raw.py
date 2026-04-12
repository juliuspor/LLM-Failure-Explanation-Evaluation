@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is not None:
        # infer element type from existing non-None elements
        inferred_element_type = None
        for item in array:
            if item is not None:
                inferred_element_type = type(item)
                break
        if inferred_element_type is None:
            # fallback to element type or object
            inferred_element_type = type(element) if element is not None else object
    elif element is not None:
        inferred_element_type = type(element)
    else:
        inferred_element_type = object

    # Build new list (functional, do not mutate input)
    new_list = ArrayUtils._copy_list_grow1(array, inferred_element_type)
    new_list[len(new_list) - 1] = element

    # If expected_type specified, ensure compatibility. Try to convert when reasonable (e.g., to str)
    if expected_type is not None:
        # If inferred is object but expected is concrete, attempt to validate/convert elements
        if inferred_element_type is object and expected_type is not object:
            # try to convert all existing elements and the new element to expected_type when possible
            converted = []
            for i, item in enumerate(new_list):
                if item is None:
                    converted.append(None)
                    continue
                if isinstance(item, expected_type):
                    converted.append(item)
                    continue
                # allow conversion to str
                if expected_type is str:
                    converted.append(str(item))
                    continue
                # allow numeric conversions
                try:
                    converted.append(expected_type(item))
                    continue
                except Exception:
                    raise TypeError(
                        f"Cannot cast list element {i} of type {type(item).__name__} to {expected_type.__name__}"
                    )
            return converted
        else:
            # Validate existing items are instances of expected_type (or None)
            for i, item in enumerate(new_list):
                if item is None:
                    continue
                if not isinstance(item, expected_type):
                    # allow conversion to str
                    if expected_type is str:
                        new_list[i] = str(item)
                        continue
                    try:
                        new_list[i] = expected_type(item)
                    except Exception:
                        raise TypeError(
                            f"Cannot cast list element {i} of type {type(item).__name__} to {expected_type.__name__}"
                        )
    return new_list