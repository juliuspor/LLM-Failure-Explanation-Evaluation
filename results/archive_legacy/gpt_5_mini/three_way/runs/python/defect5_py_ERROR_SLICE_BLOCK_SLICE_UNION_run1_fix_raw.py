@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is not None:
        if len(array) > 0:
            inferred_elem_type = None
            for itm in array:
                if itm is not None:
                    inferred_elem_type = type(itm)
                    break
            if inferred_elem_type is None:
                if element is not None:
                    inferred_elem_type = type(element)
                else:
                    inferred_elem_type = object
        else:
            if element is not None:
                inferred_elem_type = type(element)
            else:
                inferred_elem_type = object
    elif element is not None:
        inferred_elem_type = type(element)
    else:
        inferred_elem_type = object

    new_list = ArrayUtils._copy_list_grow1(array, inferred_elem_type)
    new_list[len(new_list) - 1] = element

    if expected_type is not None:
        def check_and_convert(val):
            if val is None:
                return None
            if isinstance(val, expected_type):
                return val
            try:
                return expected_type(val)
            except Exception:
                raise TypeError(f"Cannot cast element '{val}' to {expected_type.__name__}")

        for i, val in enumerate(new_list):
            if val is None:
                continue
            new_list[i] = check_and_convert(val)

    return new_list