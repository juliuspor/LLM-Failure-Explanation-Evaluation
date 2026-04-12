@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is not None:
        # If array has elements, use the type of the first element as component type
        if len(array) > 0 and array[0] is not None:
            inferred_component_type = type(array[0])
        else:
            # empty array or first element None: fall back to element type or object
            inferred_component_type = type(element) if element is not None else object
    else:
        inferred_component_type = type(element) if element is not None else object

    new_list = ArrayUtils._copy_list_grow1(array, inferred_component_type)
    new_list[len(new_list) - 1] = element

    if expected_type is not None:
        # Only raise if we truly can't determine a more specific component type (object)
        # and the expected_type is more specific than object.
        if inferred_component_type is object and expected_type is not object:
            raise TypeError(
                f"Cannot cast object list to {expected_type.__name__} list "
                f"(ClassCastException: [Ljava.lang.Object; cannot be cast to "
                f"[Ljava.lang.{expected_type.__name__};)"
            )

    return new_list