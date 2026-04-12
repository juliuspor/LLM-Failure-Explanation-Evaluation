@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is not None:
        # Try to infer element type from existing elements (first non-None element)
        inferred_elem_type = None
        for item in array:
            if item is not None:
                inferred_elem_type = type(item)
                break
    else:
        inferred_elem_type = type(element) if element is not None else None

    new_list = ArrayUtils._copy_list_grow1(array, inferred_elem_type)
    new_list[len(new_list) - 1] = element

    # If expected_type is provided, only raise if we can determine an incompatible element type.
    if expected_type is not None:
        if inferred_elem_type is not None and element is not None:
            # Both an existing element type and the new element exist: ensure compatibility
            if not issubclass(inferred_elem_type, expected_type) and not isinstance(element, expected_type):
                raise TypeError(
                    f"Cannot cast list element type {inferred_elem_type.__name__} to {expected_type.__name__}"
                )
        elif inferred_elem_type is not None and element is None:
            # Existing element type present but new element is None: allow (None can be assigned)
            pass
        elif inferred_elem_type is None and element is not None:
            # No existing elements to infer from, but we have an element: check element against expected_type
            if not isinstance(element, expected_type):
                raise TypeError(
                    f"Cannot cast element of type {type(element).__name__} to {expected_type.__name__}"
                )
        else:
            # Both inferred type and element are unknown (both None): cannot determine incompatibility — allow
            pass

    return new_list