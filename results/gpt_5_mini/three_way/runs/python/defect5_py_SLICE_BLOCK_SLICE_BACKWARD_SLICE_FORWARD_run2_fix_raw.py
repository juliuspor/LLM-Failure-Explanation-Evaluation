@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is not None:
        # Try to infer a more specific element type from the array contents
        inferred_type = None
        for item in array:
            if item is not None:
                inferred_type = type(item)
                break
        if inferred_type is None:
            # fallback to list type only if we can glean nothing from contents
            # use element type if available
            if element is not None:
                inferred_type = type(element)
            else:
                inferred_type = object
    elif element is not None:
        inferred_type = type(element)
    else:
        inferred_type = object

    # If expected_type is provided and not object, verify runtime compatibility
    if expected_type is not None and expected_type != object:
        # Check existing array elements (if any) and the new element are instances of expected_type
        incompatible = False
        if array is not None:
            for item in array:
                if item is not None and not isinstance(item, expected_type):
                    incompatible = True
                    break
        if not incompatible and element is not None and not isinstance(element, expected_type):
            incompatible = True
        if incompatible:
            raise TypeError(
                f"Cannot cast list elements to {expected_type.__name__} list "
                f"(ClassCastException: [Ljava.lang.Object; cannot be cast to [Ljava.lang.{expected_type.__name__};)"
            )

    new_list = ArrayUtils._copy_list_grow1(array, inferred_type)
    new_list[len(new_list) - 1] = element
    return new_list