@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is not None:
        # infer element type from existing contents if possible
        if len(array) == 0:
            inferred_element_type = object
        else:
            # try to determine a common element type; if mixed types, fall back to object
            first_type = type(array[0]) if array[0] is not None else type(None)
            common_type = first_type
            for item in array:
                t = type(item) if item is not None else type(None)
                if t != common_type:
                    common_type = object
                    break
            inferred_element_type = common_type
    elif element is not None:
        inferred_element_type = type(element)
    else:
        inferred_element_type = object

    new_list = ArrayUtils._copy_list_grow1(array, inferred_element_type)
    new_list[len(new_list) - 1] = element

    if expected_type is not None:
        # simulate Java-like ClassCastException when trying to cast an Object list to a more specific type
        if inferred_element_type is object and expected_type is not object:
            raise TypeError(
                f"Cannot cast object list to {expected_type.__name__} list "
                f"(ClassCastException: [Ljava.lang.Object; cannot be cast to "
                f"[Ljava.lang.{expected_type.__name__};)"
            )

    return new_list