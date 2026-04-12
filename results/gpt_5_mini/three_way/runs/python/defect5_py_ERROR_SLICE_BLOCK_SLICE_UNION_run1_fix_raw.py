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
        # If inferred_type is object, try to validate/convert elements to expected_type
        if inferred_type == object and expected_type != object:
            # Need to build a new list converting existing elements (if any) and the new element
            converted = []
            # source list to convert: if array is None, we only have the new element
            source = [] if array is None else array
            try:
                for idx, item in enumerate(source):
                    if item is None:
                        converted.append(None)
                    else:
                        if isinstance(item, expected_type):
                            converted.append(item)
                        else:
                            # attempt to construct expected_type(item) if callable
                            try:
                                converted.append(expected_type(item))
                            except Exception:
                                raise TypeError(
                                    f"Element at index {idx} of type {type(item).__name__} cannot be converted to {expected_type.__name__}"
                                )
                # handle the new element
                if element is None:
                    converted.append(None)
                else:
                    if isinstance(element, expected_type):
                        converted.append(element)
                    else:
                        try:
                            converted.append(expected_type(element))
                        except Exception:
                            raise TypeError(
                                f"Element of type {type(element).__name__} cannot be converted to {expected_type.__name__}"
                            )
            except TypeError:
                # re-raise to preserve behavior
                raise
            return converted
        # If inferred_type is not object but expected_type differs, check compatibility
        if inferred_type != object and expected_type != object and inferred_type != expected_type:
            # Allow if elements are instances of expected_type
            if array is not None and any((x is not None and not isinstance(x, expected_type)) for x in array):
                raise TypeError(
                    f"Cannot cast {inferred_type.__name__} list to {expected_type.__name__} list"
                )
            # also check the new element
            if element is not None and not isinstance(element, expected_type):
                raise TypeError(
                    f"Element of type {type(element).__name__} cannot be cast to {expected_type.__name__}"
                )

    return new_list