@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is not None:
        inferred_type = type(array)
    elif element is not None:
        inferred_type = type(element)
    else:
        inferred_type = object

    if array is None:
        new_list: List[Any] = [element]
    else:
        new_list = array.copy()
        new_list.append(element)

    if expected_type is not None:
        if inferred_type is object and array is None and element is None:
            pass
        else:
            if inferred_type is object:
                inferred_elem_type = None
            else:
                if array is not None and len(array) > 0:
                    inferred_elem_type = type(array[0])
                elif element is not None:
                    inferred_elem_type = type(element)
                else:
                    inferred_elem_type = None
            if inferred_elem_type is not None and not issubclass(inferred_elem_type, expected_type):
                raise TypeError(
                    f"Cannot cast object list to {expected_type.__name__} list "
                    f"(ClassCastException: [Ljava.lang.Object; cannot be cast to "
                    f"[Ljava.lang.{expected_type.__name__};)"
                )
    return new_list