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
        # If inferred_type is object but expected_type is more specific, attempt element-wise conversion
        if inferred_type == object and expected_type != object:
            # Build a new list converting each element to expected_type
            converted = []
            for i, item in enumerate(new_list):
                if item is None:
                    converted.append(None)
                elif isinstance(item, expected_type):
                    converted.append(item)
                else:
                    try:
                        converted.append(expected_type(item))
                    except Exception as e:
                        raise TypeError(
                            f"Cannot cast list element at index {i} ({item!r}) to {expected_type.__name__}: {e}"
                        )
            return converted
        # If both are object or expected_type is object, allow
        if inferred_type == object and expected_type == object:
            return new_list
        # For other mismatches, mimic original behavior and raise
        if inferred_type != object and expected_type is not None and inferred_type != expected_type:
            raise TypeError(
                f"Cannot cast {inferred_type.__name__} list to {expected_type.__name__} list "
                f"(ClassCastException: [Ljava.lang.{inferred_type.__name__}; cannot be cast to "
                f"[Ljava.lang.{expected_type.__name__};)"
            )

    return new_list