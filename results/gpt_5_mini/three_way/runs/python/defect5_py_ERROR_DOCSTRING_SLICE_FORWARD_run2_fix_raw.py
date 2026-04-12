@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is None:
        inferred_elem_type = type(element) if element is not None else object
        new_list = [element]
        if expected_type is not None:
            # If expected_type is provided, ensure element is compatible
            if element is not None and not isinstance(element, expected_type):
                raise TypeError(
                    f"Cannot cast object list to {expected_type.__name__} list (ClassCastException: [Ljava.lang.Object; cannot be cast to [Ljava.lang.{expected_type.__name__};)"
                )
        return new_list

    # array is not None
    # Create a shallow copy and append
    new_list = array.copy()
    new_list.append(element)

    if expected_type is not None:
        # If array appears to be an "object" list (i.e., elements are of mixed types or object)
        # then ensure all existing non-None elements are instances of expected_type
        for i, itm in enumerate(new_list):
            if itm is not None and not isinstance(itm, expected_type):
                # If the original array was of generic object type (mixed), simulate ClassCastException
                raise TypeError(
                    f"Cannot cast object list to {expected_type.__name__} list (ClassCastException: [Ljava.lang.Object; cannot be cast to [Ljava.lang.{expected_type.__name__};)"
                )
    return new_list