@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is not None:
        inferred_type = type(array)
    elif element is not None:
        inferred_type = type(element)
    elif expected_type is not None:
        inferred_type = expected_type
    else:
        inferred_type = object

    new_list = ArrayUtils._copy_list_grow1(array, inferred_type)
    new_list[len(new_list) - 1] = element

    if expected_type is not None:
        # If we couldn't infer a more specific type than object, but an expected_type
        # was requested, simulate Java's ClassCastException only when incompatible.
        if inferred_type is object and expected_type is not object:
            # If both array and element were None, but expected_type provided, accept it.
            # Only raise if we actually had an array with a different concrete type.
            # Here inferred_type is object means nothing concrete was available; allow.
            pass
        else:
            # If inferred_type is a typing/type and not compatible with expected_type, raise.
            try:
                # Use issubclass check when possible
                if isinstance(inferred_type, type) and isinstance(expected_type, type):
                    if not issubclass(inferred_type, expected_type):
                        raise TypeError(
                            f"Cannot cast {inferred_type.__name__} list to {expected_type.__name__} list"
                        )
            except TypeError:
                # issubclass can raise TypeError if inferred_type is not a class
                pass

    return new_list