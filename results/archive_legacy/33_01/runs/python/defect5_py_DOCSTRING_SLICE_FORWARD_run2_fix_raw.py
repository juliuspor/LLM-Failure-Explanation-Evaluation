@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is None:
        new_list = [element]
    else:
        new_list = array.copy()
        new_list.append(element)
    if expected_type is not None:
        try:
            from typing import get_origin, get_args
        except Exception:
            def get_origin(x):
                return getattr(x, '__origin__', None)
            def get_args(x):
                return getattr(x, '__args__', ())
        origin = get_origin(expected_type)
        if origin is None:
            valid_types = (expected_type,)
        elif origin is Union:
            args = get_args(expected_type)
            valid_types = tuple(a for a in args if isinstance(a, type))
        else:
            valid_types = tuple(a for a in get_args(expected_type) if isinstance(a, type))
        if not valid_types:
            if expected_type is object:
                return new_list
            raise TypeError(f"expected_type must be a class or typing.Union of classes, got: {expected_type}")
        elem_type = type(element) if element is not None else object
        if elem_type is object and element is None:
            if object not in valid_types and not any(t is object for t in valid_types):
                raise TypeError(
                    f"Cannot cast object list to {getattr(expected_type, '__name__', str(expected_type))} list (ClassCastException: [Ljava.lang.Object; cannot be cast to [Ljava.lang.{getattr(expected_type, '__name__', str(expected_type))};)"
                )
        else:
            if not isinstance(element, valid_types):
                raise TypeError(
                    f"Cannot cast object list to {getattr(expected_type, '__name__', str(expected_type))} list (ClassCastException: [Ljava.lang.Object; cannot be cast to [Ljava.lang.{getattr(expected_type, '__name__', str(expected_type))};)"
                )
    return new_list