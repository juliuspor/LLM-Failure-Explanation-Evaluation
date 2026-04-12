@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is not None and len(array) > 0:
        # Infer element type from first non-None element in the array
        inferred_elem_type = None
        for item in array:
            if item is not None:
                inferred_elem_type = type(item)
                break
        if inferred_elem_type is None:
            # All elements are None -> fallback to object
            inferred_elem_type = object
    elif element is not None:
        inferred_elem_type = type(element)
    else:
        inferred_elem_type = object

    new_list = ArrayUtils._copy_list_grow1(array, inferred_elem_type)
    new_list[len(new_list) - 1] = element

    if expected_type is not None:
        # Simulate a Java-like ClassCastException when we only know element type is object
        if inferred_elem_type is object and expected_type is not object:
            raise TypeError(f"Cannot cast object list to {expected_type.__name__} list")

    return new_list