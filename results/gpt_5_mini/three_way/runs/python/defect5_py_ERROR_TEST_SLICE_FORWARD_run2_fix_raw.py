@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is not None:
        # preserve existing list elements and inferred component type from array
        inferred_type = type(array[0]) if len(array) > 0 and array[0] is not None else object
    elif element is not None:
        inferred_type = type(element)
    else:
        inferred_type = object

    # If caller provided an expected_type, honor it for validation
    if expected_type is not None:
        # If both array and element are None, we cannot infer a more specific type
        if array is None and element is None:
            if expected_type != object:
                # Simulate Java ClassCastException by raising TypeError
                raise TypeError(
                    f"Cannot cast object list to {expected_type.__name__} list (ClassCastException: [Ljava.lang.Object; cannot be cast to [Ljava.lang.{expected_type.__name__};)"
                )
        else:
            # If we have an inferred type that is object but expected_type is more specific,
            # and element is not an instance of expected_type (when element present), raise
            if inferred_type is object and element is not None and not isinstance(element, expected_type):
                raise TypeError(
                    f"Element of type {type(element).__name__} cannot be added to list of {expected_type.__name__}"
                )

    new_list = ArrayUtils._copy_list_grow1(array, inferred_type)
    new_list[len(new_list) - 1] = element
    return new_list