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
        # If we have no specific inferred type (object), perform runtime checks on elements
        if inferred_type == object and expected_type != object:
            # If array is not None, validate existing elements
            if array is not None:
                for i, val in enumerate(array):
                    if val is not None and not isinstance(val, expected_type):
                        raise TypeError(
                            f"Element at index {i} is of type {type(val).__name__}; cannot cast to {expected_type.__name__}"
                        )
            # Check the new element as well
            if element is not None and not isinstance(element, expected_type):
                raise TypeError(
                    f"Element to add is of type {type(element).__name__}; cannot cast to {expected_type.__name__}"
                )
        # If inferred_type is not object but types mismatch, keep original behavior: raise
        elif inferred_type != object and inferred_type != expected_type and expected_type != object:
            raise TypeError(
                f"Cannot cast {inferred_type.__name__} list to {expected_type.__name__} list"
            )

    return new_list