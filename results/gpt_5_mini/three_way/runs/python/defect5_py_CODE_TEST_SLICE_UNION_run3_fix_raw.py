@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is not None:
        # Infer element type from existing elements: pick first non-None element's type
        inferred_element_type: Type = object
        for item in array:
            if item is not None:
                inferred_element_type = type(item)
                break
    elif element is not None:
        inferred_element_type = type(element)
    else:
        inferred_element_type = object

    new_list = ArrayUtils._copy_list_grow1(array, inferred_element_type)
    # _copy_list_grow1 guarantees at least one slot (appended None) when array is not None,
    # and returns [None] when array is None, so safe to set last element by index.
    if len(new_list) == 0:
        new_list.append(element)
    else:
        new_list[-1] = element

    if expected_type is not None:
        # If we couldn't infer a concrete element type (object), and expected_type is more specific,
        # simulate Java-style ClassCastException by raising TypeError.
        if inferred_element_type is object and expected_type is not object:
            raise TypeError(
                f"Cannot cast object list to {expected_type.__name__} list "
                f"(ClassCastException: [Ljava.lang.Object; cannot be cast to "
                f"[Ljava.lang.{expected_type.__name__};)"
            )

    return new_list