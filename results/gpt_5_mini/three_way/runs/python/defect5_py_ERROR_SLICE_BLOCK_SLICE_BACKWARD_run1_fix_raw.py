@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is not None:
        # Infer component type from contents (first non-None element)
        inferred_component_type = None
        for item in array:
            if item is not None:
                inferred_component_type = type(item)
                break
        if inferred_component_type is None:
            inferred_component_type = object
    elif element is not None:
        inferred_component_type = type(element)
    else:
        inferred_component_type = object

    # create new list with one extra slot and set the last element
    new_list = ArrayUtils._copy_list_grow1(array, inferred_component_type)
    new_list[len(new_list) - 1] = element

    # If an expected_type is given, validate compatibility
    if expected_type is not None:
        # If array had concrete component type that is not compatible with expected_type, raise
        if inferred_component_type is not object and not issubclass(inferred_component_type, expected_type):
            raise TypeError(
                f"Cannot cast {inferred_component_type.__name__} list to {expected_type.__name__} list "
                f"(ClassCastException: [Ljava.lang.{inferred_component_type.__name__}; cannot be cast to "
                f"[Ljava.lang.{expected_type.__name__};)"
            )
        # If inferred is object but array contains elements that are incompatible with expected_type, raise
        if inferred_component_type is object and array is not None:
            for i, item in enumerate(array):
                if item is not None and not isinstance(item, expected_type):
                    raise TypeError(
                        f"Cannot cast Object list to {expected_type.__name__} list "
                        f"(ClassCastException: [Ljava.lang.Object; cannot be cast to "
                        f"[Ljava.lang.{expected_type.__name__};)\nIncompatible element at index {i}: {type(item).__name__}"
                    )
        # If element itself is incompatible, also raise
        if element is not None and not isinstance(element, expected_type):
            raise TypeError(
                f"Element of type {type(element).__name__} cannot be added to {expected_type.__name__} list"
            )

    return new_list