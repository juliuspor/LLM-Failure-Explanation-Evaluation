@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is None:
        inferred_type = type(element) if element is not None else object
        new_list: List[T] = [element]
        if expected_type is not None and inferred_type == object and expected_type is not object:
            return new_list if element is None else ([element] if isinstance(element, expected_type) else (_ for _ in ()).throw(TypeError(f"Cannot cast object list to {expected_type.__name__} list (ClassCastException: [Ljava.lang.Object; cannot be cast to [Ljava.lang.{expected_type.__name__};)")))
        if expected_type is not None and element is not None and not isinstance(element, expected_type):
            raise TypeError(f"Cannot cast object list to {expected_type.__name__} list (ClassCastException: [Ljava.lang.Object; cannot be cast to [Ljava.lang.{expected_type.__name__};)")
        return new_list
    inferred_type = object
    for item in array:
        if item is not None:
            inferred_type = type(item)
            break
    if inferred_type is object and expected_type is not None and expected_type is not object:
        inferred_type = expected_type
    if expected_type is not None:
        for i, item in enumerate(array):
            if item is not None and not isinstance(item, expected_type):
                raise TypeError(f"Cannot cast object list to {expected_type.__name__} list (ClassCastException: [Ljava.lang.Object; cannot be cast to [Ljava.lang.{expected_type.__name__};)")
        if element is not None and not isinstance(element, expected_type):
            raise TypeError(f"Cannot cast object list to {expected_type.__name__} list (ClassCastException: [Ljava.lang.Object; cannot be cast to [Ljava.lang.{expected_type.__name__};)")
    new_list = array.copy()
    new_list.append(element)
    return new_list