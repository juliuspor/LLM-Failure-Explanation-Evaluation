@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is not None:
        # Try to infer the element type from the array contents: find first non-None element
        inferred_type = object
        try:
            # Handle numpy arrays or other objects with dtype
            import numpy as _np
            if hasattr(array, 'dtype'):
                # numpy dtype may map to a type; dtype.type gives the scalar type
                inferred_type = getattr(array.dtype, 'type', object) or object
            else:
                # For sequences, find first non-None element
                for item in array:
                    if item is not None:
                        inferred_type = item.__class__
                        break
        except Exception:
            # Fallback: try to inspect sequence elements
            inferred_type = object
            for item in array:
                if item is not None:
                    inferred_type = item.__class__
                    break
    elif element is not None:
        inferred_type = element.__class__
    else:
        inferred_type = object

    new_list = ArrayUtils._copy_list_grow1(array, inferred_type)
    new_list[len(new_list) - 1] = element

    if expected_type is not None:
        # Only raise if we were able to infer a concrete type that is incompatible
        if inferred_type is not object and not issubclass(inferred_type, expected_type):
            raise TypeError(
                f"Cannot cast object list to {expected_type.__name__} list "
                f"(ClassCastException: [Ljava.lang.{inferred_type.__name__}; cannot be cast to "
                f"[Ljava.lang.{expected_type.__name__};)"
            )
    return new_list