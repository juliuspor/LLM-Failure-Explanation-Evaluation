@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is not None:
        # Determine component type from existing elements: find first non-None element
        inferred_type = None
        for item in array:
            if item is not None:
                inferred_type = type(item)
                break
        if inferred_type is None:
            # all elements are None (or array empty)
            inferred_type = object
    elif element is not None:
        inferred_type = type(element)
    else:
        inferred_type = object

    new_list = ArrayUtils._copy_list_grow1(array, inferred_type)
    new_list[len(new_list) - 1] = element

    if expected_type is not None:
        # Only raise if we have a concrete inferred type that is object (unknown)
        # and the provided element contradicts the expected_type, or if inferred
        # concrete type exists and is incompatible with expected_type.
        if inferred_type is object:
            # If both array and element provide no type information, allow it.
            if array is None and element is None:
                pass
            elif element is not None and not isinstance(element, expected_type):
                raise TypeError(
                    f"Cannot cast object list to {expected_type.__name__} list "
                    f"(ClassCastException: [Ljava.lang.Object; cannot be cast to "
                    f"[Ljava.lang.{expected_type.__name__};)"
                )
        else:
            # inferred_type is concrete; ensure it's compatible with expected_type
            if not issubclass(inferred_type, expected_type):
                raise TypeError(
                    f"Cannot cast {inferred_type.__name__} list to {expected_type.__name__} list "
                    f"(ClassCastException: [Ljava.lang.{inferred_type.__name__}; cannot be cast to "
                    f"[Ljava.lang.{expected_type.__name__};)"
                )

    return new_list