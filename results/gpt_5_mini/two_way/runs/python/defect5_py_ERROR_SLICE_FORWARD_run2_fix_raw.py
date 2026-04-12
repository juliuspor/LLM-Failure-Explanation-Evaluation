@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is not None:
        # infer element type from first non-None element in array if possible
        inferred_type = None
        for itm in array:
            if itm is not None:
                inferred_type = type(itm)
                break
        if inferred_type is None:
            # all elements are None -> fall back to object
            inferred_type = object
    elif element is not None:
        inferred_type = type(element)
    else:
        inferred_type = object

    new_list = ArrayUtils._copy_list_grow1(array, inferred_type)
    new_list[len(new_list) - 1] = element

    if expected_type is not None:
        # If expected_type is not object, ensure that the inferred element type and
        # the new element are compatible with expected_type. If inferred_type is object
        # but element is not None, we check the element instance. If both array and
        # element provide no type information (object), simulate cast failure.
        if expected_type != object:
            # check existing elements in array
            if array is not None:
                for i, itm in enumerate(array):
                    if itm is not None and not isinstance(itm, expected_type):
                        raise TypeError(
                            f"Cannot cast list element at index {i} of type {type(itm).__name__} to {expected_type.__name__}"
                        )
                # if array had only None elements, but no element to infer from, and element is None -> fail
                if all(itm is None for itm in array) and element is None:
                    raise TypeError(
                        f"Cannot cast object list to {expected_type.__name__} list (ClassCastException)"
                    )
            # check the new element
            if element is not None and not isinstance(element, expected_type):
                raise TypeError(
                    f"Cannot cast element of type {type(element).__name__} to {expected_type.__name__}"
                )

    return new_list