@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is not None:
        inferred_type = type(array)
    elif element is not None:
        inferred_type = type(element)
    else:
        inferred_type = object

    new_list = ArrayUtils._copy_list_grow1(array, inferred_type)
    new_list[len(new_list) - 1] = element

    if expected_type is not None:
        # Normalize expected_type if it's a typing construct (e.g., List[int])
        try:
            from typing import get_origin
        except Exception:
            get_origin = lambda x: None

        origin = get_origin(expected_type) if expected_type is not None else None
        type_to_check = origin if origin is not None else expected_type

        # Only perform isinstance check if type_to_check is a real type/class
        if isinstance(type_to_check, type):
            # If we started with an object-list (inferred_type == object) but an explicit
            # concrete expected_type was requested, simulate a Java ClassCastException
            if inferred_type == object and type_to_check is not object:
                raise TypeError(
                    f"Cannot cast object list to {type_to_check.__name__} list "
                    f"(ClassCastException: [Ljava.lang.Object; cannot be cast to "
                    f"[Ljava.lang.{type_to_check.__name__};)"
                )
            # If element is not None and not instance of expected component type, raise
            if element is not None and not isinstance(element, type_to_check):
                raise TypeError(f"Element of type {type(element).__name__} cannot be assigned to list of {type_to_check.__name__}")
        else:
            # expected_type isn't a real type (e.g., a typing.Parameterized), skip strict isinstance check
            # but still simulate cast failure if inferred_type was object and expected_type is not 'object'
            if inferred_type == object and expected_type is not object:
                # Cannot reliably check parameterized/complex typing, so raise to mirror Java behavior
                raise TypeError(
                    f"Cannot cast object list to {getattr(expected_type, '__repr__', lambda: str(expected_type))()} list "
                    f"(ClassCastException: [Ljava.lang.Object; cannot be cast to [Ljava.lang.{getattr(expected_type, '__name__', str(expected_type))};)"
                )

    return new_list