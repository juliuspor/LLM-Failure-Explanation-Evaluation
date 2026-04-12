@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is not None and len(array) > 0:
        # infer component type from first existing element
        comp_type = type(array[0]) if array[0] is not None else object
    elif element is not None:
        comp_type = type(element)
    else:
        comp_type = object

    new_list = ArrayUtils._copy_list_grow1(array, comp_type)
    new_list[len(new_list) - 1] = element

    if expected_type is not None:
        # If component type is unknown/object but expected_type is specific, simulate Java cast failure
        if comp_type == object and expected_type != object:
            # If both array and element are None, allow creating a list of None for expected_type
            if not (array is None and element is None):
                raise TypeError(
                    f"Cannot cast object list to {expected_type.__name__} list "
                    f"(ClassCastException: [Ljava.lang.Object; cannot be cast to "
                    f"[Ljava.lang.{expected_type.__name__};)"
                )
    return new_list