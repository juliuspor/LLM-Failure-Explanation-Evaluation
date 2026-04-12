@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is None:
        base_list: List[T] = []
    else:
        base_list = array.copy()

    base_list.append(element)

    if expected_type is not None:
        converted: List[T] = []
        for i, item in enumerate(base_list):
            if item is None:
                converted.append(None)  # allow None values
                continue
            if isinstance(item, expected_type):
                converted.append(item)
                continue
            # attempt to coerce/convert
            try:
                converted_item = expected_type(item)
            except Exception:
                raise TypeError(
                    f"Cannot convert element at index {i} ({item!r}) to {expected_type.__name__}"
                )
            # After conversion, ensure type matches
            if not isinstance(converted_item, expected_type):
                raise TypeError(
                    f"Converted element at index {i} is not of type {expected_type.__name__}"
                )
            converted.append(converted_item)
        return converted

    return base_list