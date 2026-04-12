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
        # If expected_type is object, any list is acceptable
        if expected_type is object:
            return new_list

        # If array is None, only need to check the new element
        if array is None:
            if element is not None and not isinstance(element, expected_type):
                raise TypeError(
                    f"Cannot cast to {expected_type.__name__} list: element of type {type(element).__name__} at index 0 is not compatible"
                )
            return new_list

        # Verify every non-None element in the resulting list is instance of expected_type
        for idx, itm in enumerate(new_list):
            if itm is None:
                # None is acceptable for reference types; skip checking
                continue
            if not isinstance(itm, expected_type):
                raise TypeError(
                    f"Cannot cast to {expected_type.__name__} list: element at index {idx} is of type {type(itm).__name__}"
                )
    return new_list