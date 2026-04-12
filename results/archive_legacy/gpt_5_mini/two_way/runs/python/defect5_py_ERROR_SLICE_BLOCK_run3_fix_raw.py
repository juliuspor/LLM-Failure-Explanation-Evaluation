@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is not None:
        inferred_type = type(array[0]) if len(array) > 0 else object
    elif element is not None:
        inferred_type = type(element)
    else:
        inferred_type = object

    new_list = ArrayUtils._copy_list_grow1(array, inferred_type)
    new_list[len(new_list) - 1] = element

    if expected_type is not None:
        if inferred_type == object and expected_type != object:
            # attempt to convert existing elements (excluding the appended element which we'll also try)
            converted = []
            try:
                for item in new_list:
                    if item is None:
                        converted.append(None)
                    else:
                        converted.append(expected_type(item))
            except Exception as e:
                raise TypeError(
                    f"Cannot convert object list to {expected_type.__name__} list: {e}"
                )
            return converted
    return new_list