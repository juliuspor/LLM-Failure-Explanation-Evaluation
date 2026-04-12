@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is not None:
        # try to infer element type from existing contents: first non-None element
        inferred_element_type = None
        for item in array:
            if item is not None:
                inferred_element_type = type(item)
                break
    elif element is not None:
        inferred_element_type = type(element)
    else:
        inferred_element_type = None

    new_list = ArrayUtils._copy_list_grow1(array, inferred_element_type)
    new_list[len(new_list) - 1] = element

    if expected_type is not None:
        # If we could infer an element type, ensure it's compatible with expected_type.
        # If nothing could be inferred (all elements and element are None), treat as compatible.
        if inferred_element_type is not None:
            # allow subclassing compatibility
            try:
                is_compatible = issubclass(inferred_element_type, expected_type)
            except TypeError:
                # expected_type might be typing constructs; fall back to direct equality
                is_compatible = inferred_element_type == expected_type
            if not is_compatible:
                raise TypeError(
                    f"Cannot cast {inferred_element_type.__name__} list to {expected_type.__name__} list "
                    f"(ClassCastException: [L{inferred_element_type.__name__}; cannot be cast to [L{expected_type.__name__};)"
                )

    return new_list