@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is None:
        # Start from empty and append element (with optional type check/coercion)
        new_list: List[T] = [None]
        new_list[0] = element
        if expected_type is not None and element is not None and not isinstance(element, expected_type):
            try:
                new_list[0] = expected_type(element)
            except Exception:
                raise TypeError(
                    f"Cannot cast element of type {type(element).__name__} to {expected_type.__name__}"
                )
        return new_list

    # array is not None: create a shallow copy and append element
    new_list = array.copy()
    # Append with possible type enforcement
    if expected_type is not None and element is not None and not isinstance(element, expected_type):
        try:
            coerced = expected_type(element)
        except Exception:
            raise TypeError(
                f"Cannot cast element of type {type(element).__name__} to {expected_type.__name__}"
            )
        new_list.append(coerced)
    else:
        new_list.append(element)

    return new_list