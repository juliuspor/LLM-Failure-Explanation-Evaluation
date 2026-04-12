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
        if inferred_type is not object:
            try:
                if not issubclass(inferred_type, expected_type):
                    raise TypeError(f"Cannot cast {inferred_type.__name__} list to {expected_type.__name__} list")
            except TypeError:
                raise
            except Exception:
                pass
        else:
            for i, elem in enumerate(new_list):
                if elem is None:
                    continue
                if not isinstance(elem, expected_type):
                    raise TypeError(f"Element at index {i} (type {type(elem).__name__}) cannot be cast to {expected_type.__name__}")
    return new_list