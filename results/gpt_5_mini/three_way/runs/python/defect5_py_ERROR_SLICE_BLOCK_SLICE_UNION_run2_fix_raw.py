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
        # If inferred_type is object (no concrete list type), validate/convert elements to expected_type
        if inferred_type == object and expected_type != object:
            # Validate existing elements in the new list (except the trailing None already replaced)
            for i, val in enumerate(new_list):
                if val is None:
                    continue
                if not isinstance(val, expected_type):
                    # Try to coerce/convert
                    try:
                        new_list[i] = expected_type(val)  # type: ignore
                    except Exception:
                        raise TypeError(
                            f"Cannot cast element at index {i} ({type(val).__name__}) to {expected_type.__name__}"
                        )
        else:
            # If array has a concrete type that's not object but expected_type differs, ensure compatibility
            if inferred_type != object and expected_type != object and inferred_type != expected_type:
                # Check elements for compatibility
                for i, val in enumerate(new_list):
                    if val is None:
                        continue
                    if not isinstance(val, expected_type):
                        try:
                            new_list[i] = expected_type(val)  # type: ignore
                        except Exception:
                            raise TypeError(
                                f"Cannot cast element at index {i} ({type(val).__name__}) to {expected_type.__name__}"
                            )

    return new_list