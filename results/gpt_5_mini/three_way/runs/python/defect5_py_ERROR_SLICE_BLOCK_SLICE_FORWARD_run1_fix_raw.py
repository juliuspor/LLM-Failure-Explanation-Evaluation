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
        # If we inferred a generic object list but an expected_type is requested,
        # try to ensure all elements are instances of expected_type. Convert where possible.
        if inferred_type == object and expected_type != object:
            # Validate existing elements (except the appended None placeholder handled above)
            validated = []
            for item in new_list:
                if item is None:
                    # None is allowed; keep as is
                    validated.append(None)
                elif isinstance(item, expected_type):
                    validated.append(item)
                else:
                    # Attempt a conversion if possible by calling the expected_type on the item
                    try:
                        converted = expected_type(item)
                    except Exception:
                        raise TypeError(
                            f"Cannot cast object list element of type {type(item).__name__} to {expected_type.__name__}"
                        )
                    else:
                        validated.append(converted)
            return validated
    return new_list