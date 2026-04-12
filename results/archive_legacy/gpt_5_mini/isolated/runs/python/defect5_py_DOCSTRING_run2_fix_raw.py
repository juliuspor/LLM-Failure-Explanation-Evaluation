@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is None:
        result = []
    else:
        result = array.copy()
    result.append(element)
    if expected_type is not None:
        if not isinstance(expected_type, type):
            raise TypeError("expected_type must be a type")
        if array is None:
            if element is not None and not isinstance(element, expected_type):
                raise TypeError(f"Cannot cast object list to {expected_type.__name__} list (ClassCastException: [Ljava.lang.Object; cannot be cast to [Ljava.lang.{expected_type.__name__};)")
        else:
            for i, v in enumerate(result):
                if v is not None and not isinstance(v, expected_type):
                    raise TypeError(f"Cannot cast object list to {expected_type.__name__} list (ClassCastException: [Ljava.lang.Object; cannot be cast to [Ljava.lang.{expected_type.__name__};)")
    return result