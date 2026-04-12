@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is None:
        # treat as empty list
        new_list = [element]
    else:
        new_list = array.copy()
        new_list.append(element)

    # If expected_type provided, ensure element is compatible (simulate Java cast failure)
    if expected_type is not None and element is not None:
        # For generics, check isinstance; if not, raise TypeError
        if not isinstance(element, expected_type):
            raise TypeError(
                f"Cannot cast element of type {type(element).__name__} to {expected_type.__name__}"
            )

    return new_list