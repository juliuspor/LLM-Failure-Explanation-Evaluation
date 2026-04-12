@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is not None and len(array) > 0:
        inferred_component_type = type(array[0])
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
        # Simulate Java-style ClassCastException when component type is unknown (object)
        if inferred_component_type is object and expected_type is not object:
            raise TypeError(
                f"Cannot cast object list to {expected_type.__name__} list "
                f"(ClassCastException: [Ljava.lang.Object; cannot be cast to "
                f"[Ljava.lang.{expected_type.__name__};)"
            )
    return new_list