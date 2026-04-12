@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is None:
        base = []
    else:
        base = array.copy()

    new_list = base + [element]

    if expected_type is not None:
        # Only perform runtime isinstance check if expected_type is a concrete class or tuple of classes.
        try:
            # typing constructs like list[int] have no __mro__, get_origin helps detect them
            from typing import get_origin
            origin = get_origin(expected_type)
        except Exception:
            origin = None

        is_concrete = False
        if origin is None:
            # expected_type is not a typing construct; ensure it's a type or tuple of types
            if isinstance(expected_type, type) or (
                isinstance(expected_type, tuple) and all(isinstance(t, type) for t in expected_type)
            ):
                is_concrete = True

        if is_concrete:
            # Only check the newly added element to simulate a component-type cast
            try:
                if element is not None and not isinstance(element, expected_type):
                    raise TypeError(
                        f"Cannot cast element of type {type(element).__name__} to {expected_type.__name__}"
                    )
            except TypeError:
                # Re-raise with a clearer message
                raise TypeError(
                    f"Type check failed: expected_type must be a concrete type for isinstance checks."
                )
        else:
            # Cannot perform isinstance for typing constructs; raise informative error to mirror Java cast failure
            raise TypeError(
                f"Cannot perform runtime type check with typing construct '{expected_type}'. Provide a concrete type instead."
            )

    return new_list