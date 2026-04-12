@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is not None:
        # Do not modify the original array; create a shallow copy and append
        new_list: List[T] = array.copy()
        new_list.append(element)
        inferred_type = type(array)
    else:
        # Create a new single-element list
        new_list = [element]
        # inferred_type should reflect element if present, else object
        inferred_type = type(element) if element is not None else object

    # Simulate Java-like cast failure: if expected_type specified and we don't have
    # a concrete inferred component type (object) but expected_type is more specific,
    # raise TypeError as the original code attempted to do.
    if expected_type is not None:
        if inferred_type is object and expected_type is not object:
            raise TypeError(
                f"Cannot cast object list to {expected_type.__name__} list "
                f"(ClassCastException: [Ljava.lang.Object; cannot be cast to "
                f"[Ljava.lang.{expected_type.__name__};)"
            )
    return new_list