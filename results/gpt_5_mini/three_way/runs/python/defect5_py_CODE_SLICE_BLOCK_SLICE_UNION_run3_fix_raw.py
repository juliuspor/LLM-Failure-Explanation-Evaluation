@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is not None:
        # Infer element type from first non-None element in the list, if possible
        inferred_type = None
        for item in array:
            if item is not None:
                inferred_type = type(item)
                break
        if inferred_type is None:
            # no non-None elements; fall back to object's type if element provided
            inferred_type = type(element) if element is not None else object
    elif element is not None:
        inferred_type = type(element)
    else:
        inferred_type = object

    new_list = ArrayUtils._copy_list_grow1(array, inferred_type)
    new_list[len(new_list) - 1] = element

    if expected_type is not None:
        if inferred_type == object and expected_type != object:
            raise TypeError(
                f"Cannot cast object list to {expected_type.__name__} list">
            )

    return new_list