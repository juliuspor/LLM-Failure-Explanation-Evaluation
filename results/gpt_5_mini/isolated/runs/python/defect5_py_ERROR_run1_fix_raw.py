@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is not None:
        # infer component type from existing elements: find first non-None element
        inferred_component_type = None
        for item in array:
            if item is not None:
                inferred_component_type = type(item)
                break
        if inferred_component_type is None:
            # no non-None elements, fall back to object
            inferred_component_type = object
    elif element is not None:
        inferred_component_type = type(element)
    else:
        inferred_component_type = object

    new_list = ArrayUtils._copy_list_grow1(array, inferred_component_type)
    new_list[len(new_list) - 1] = element

    if expected_type is not None:
        # If we only know object component type but expected is more specific, that's an error
        if inferred_component_type == object and expected_type != object:
            raise TypeError(
                f"Cannot cast object list to {expected_type.__name__} list "
                f"(ClassCastException: [Ljava.lang.Object; cannot be cast to "
                f"[Ljava.lang.{expected_type.__name__};)"
            )
        # If we have a more specific inferred type, ensure compatibility with expected_type
        if inferred_component_type is not object and not issubclass(inferred_component_type, expected_type):
            raise TypeError(
                f"Cannot cast {inferred_component_type.__name__} list to {expected_type.__name__} list "
                f"(ClassCastException: [Ljava.lang.{inferred_component_type.__name__}; cannot be cast to "
                f"[Ljava.lang.{expected_type.__name__};)"
            )

    return new_list