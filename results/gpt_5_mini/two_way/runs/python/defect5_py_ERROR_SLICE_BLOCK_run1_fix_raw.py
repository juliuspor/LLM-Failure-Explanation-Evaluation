@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is not None:
        # infer type from existing elements (first non-None element)
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
        # If expected_type is object, nothing to check
        if expected_type is not object:
            # If we have a concrete inferred type that's incompatible with expected_type,
            # try to ensure elements are instances of expected_type or coerce the new element.
            # Check existing elements: if any non-None element is not instance of expected_type,
            # we won't attempt to coerce them (cannot safely change), so raise TypeError.
            if array is not None:
                for idx, item in enumerate(array):
                    if item is not None and not isinstance(item, expected_type):
                        raise TypeError(
                            f"Existing element at index {idx} of type {type(item).__name__} "
                            f"cannot be treated as {expected_type.__name__}"
                        )
            # Now check the new element: if it's not instance, try to coerce if possible
            if element is not None and not isinstance(element, expected_type):
                try:
                    # Attempt to coerce by calling expected_type(element) if it's callable
                    if callable(expected_type):
                        coerced = expected_type(element)
                        new_list[len(new_list) - 1] = coerced
                    else:
                        raise TypeError(
                            f"Element of type {type(element).__name__} cannot be cast to {expected_type.__name__}"
                        )
                except Exception as e:
                    raise TypeError(
                        f"Element of type {type(element).__name__} cannot be cast to {expected_type.__name__}: {e}"
                    )

    return new_list