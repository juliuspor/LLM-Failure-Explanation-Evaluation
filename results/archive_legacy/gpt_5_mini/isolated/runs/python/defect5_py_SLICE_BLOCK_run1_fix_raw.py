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
        safe_name = getattr(expected_type, "__name__", repr(expected_type))
        if array is None:
            if element is None:
                pass
            else:
                if not isinstance(element, expected_type):
                    raise TypeError(f"Cannot cast element of type {type(element).__name__} to {safe_name} (ClassCastException)")
        else:
            if len(array) == 0:
                pass
            else:
                for i, item in enumerate(new_list[:-1]):
                    if item is None:
                        continue
                    if not isinstance(item, expected_type):
                        raise TypeError(f"Cannot cast element at index {i} of type {type(item).__name__} to {safe_name} (ClassCastException)")
                last = new_list[-1]
                if last is not None and not isinstance(last, expected_type):
                    raise TypeError(f"Cannot cast element of type {type(last).__name__} to {safe_name} (ClassCastException)")
    return new_list