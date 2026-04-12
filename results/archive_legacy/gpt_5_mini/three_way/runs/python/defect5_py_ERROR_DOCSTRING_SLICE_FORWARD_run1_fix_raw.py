@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is not None:
        new_list = array.copy()
        new_list.append(element)
        if expected_type is not None:
            for i, it in enumerate(new_list):
                if it is not None and not isinstance(it, expected_type):
                    raise TypeError(
                        f"Cannot cast list element at index {i} to {expected_type.__name__}"
                    )
        return new_list
    else:
        if element is None:
            if expected_type is not None and expected_type is not object:
                raise TypeError(
                    f"Cannot cast object list to {expected_type.__name__} list (ClassCastException: [Ljava.lang.Object; cannot be cast to [Ljava.lang.{expected_type.__name__};)"
                )
            return [None]
        else:
            if expected_type is not None and not isinstance(element, expected_type):
                raise TypeError(
                    f"Cannot add element of type {type(element).__name__} to list of {expected_type.__name__}"
                )
            return [element]