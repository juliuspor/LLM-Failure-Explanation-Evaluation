@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is None:
        # When array is None, we treat as empty list. Infer component type from element if present
        inferred_component_type = type(element) if element is not None else object
    else:
        # If array provided, try to infer component type from first element if available
        if len(array) > 0 and array[0] is not None:
            inferred_component_type = type(array[0])
        else:
            # Fallback: if expected_type given use that, else object
            inferred_component_type = expected_type if expected_type is not None else object

    # If expected_type provided, ensure compatibility
    if expected_type is not None and inferred_component_type is not object:
        # Rough compatibility check: element type must be subclass of expected_type or vice versa
        try:
            # Use issubclass when possible
            if isinstance(inferred_component_type, type) and isinstance(expected_type, type):
                if not issubclass(inferred_component_type, expected_type) and not issubclass(expected_type, inferred_component_type):
                    # If neither is subclass of the other, reject when element (if present) doesn't match
                    if element is not None and not isinstance(element, expected_type):
                        raise TypeError(
                            f"Cannot cast {inferred_component_type.__name__} list to {expected_type.__name__} list "
                            f"(ClassCastException: [Ljava.lang.{inferred_component_type.__name__}; cannot be cast to [Ljava.lang.{expected_type.__name__};)"
                        )
        except TypeError:
            # In case inferred_component_type is not a class, skip strict checks
            pass

    if array is None:
        # simple case: return new list with the single element
        return [element]

    new_list = ArrayUtils._copy_list_grow1(array, inferred_component_type)
    new_list[len(new_list) - 1] = element
    return new_list