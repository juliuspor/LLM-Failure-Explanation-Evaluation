@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is not None:
        inferred_type = type(array)
    elif element is not None:
        inferred_type = type(element)
    else:
        inferred_type = object

    # If we only have a generic object inferred type but an expected_type was
    # supplied, use the expected_type as the inferred type to avoid a spurious
    # ClassCast-like error. This also mirrors the intent of enforcing a
    # component type when one is provided.
    if inferred_type == object and expected_type is not None:
        inferred_type = expected_type

    new_list = ArrayUtils._copy_list_grow1(array, inferred_type)
    new_list[len(new_list) - 1] = element

    if expected_type is not None:
        # If we have an actual element, ensure it matches expected_type at runtime.
        if element is not None and not isinstance(element, expected_type):
            raise TypeError(
                f"Cannot cast element of type {type(element).__name__} to {expected_type.__name__}"
            )

    return new_list