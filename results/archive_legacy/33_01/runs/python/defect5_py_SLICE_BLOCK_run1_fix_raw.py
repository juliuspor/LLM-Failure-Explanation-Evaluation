@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is not None:
        inferred_type = None
        for item in array:
            if item is not None:
                inferred_type = type(item)
                break
        if inferred_type is None:
            inferred_type = object
    elif element is not None:
        inferred_type = type(element)
    else:
        inferred_type = object

    new_list = ArrayUtils._copy_list_grow1(array, inferred_type)
    new_list[len(new_list) - 1] = element

    if expected_type is not None:
        if inferred_type == object:
            if array is None:
                pass
            else:
                for i, itm in enumerate(array):
                    if itm is None:
                        continue
                    if not isinstance(itm, expected_type):
                        raise TypeError(
                            f"Cannot cast list to {expected_type.__name__} list (element at index {i} is of type {type(itm).__name__})"
                        )
        else:
            if not issubclass(inferred_type, expected_type):
                raise TypeError(
                    f"Cannot cast list to {expected_type.__name__} list (inferred element type {inferred_type.__name__} is not assignable to {expected_type.__name__})"
                )
    return new_list