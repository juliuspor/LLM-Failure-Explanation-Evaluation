@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is not None:
        # infer element/component type from first non-None element if possible
        inferred_component_type = None
        for item in array:
            if item is not None:
                inferred_component_type = type(item)
                break
        if inferred_component_type is None:
            # array exists but all elements are None or array is empty; fall back to object
            inferred_component_type = object
    elif element is not None:
        inferred_component_type = type(element)
    else:
        inferred_component_type = object

    new_list = ArrayUtils._copy_list_grow1(array, inferred_component_type)
    # Ensure new_list has at least one slot at the end
    if len(new_list) == 0:
        new_list.append(element)
    else:
        new_list[len(new_list) - 1] = element

    if expected_type is not None:
        # if we couldn't determine a more specific component type (object), simulate cast failure
        if inferred_component_type is object and expected_type is not object:
            raise TypeError(
                f"Cannot cast object list to {expected_type.__name__} list "
                f"(ClassCastException: [Ljava.lang.Object; cannot be cast to "
                f"[Ljava.lang.{expected_type.__name__};)"
            )
    return new_list