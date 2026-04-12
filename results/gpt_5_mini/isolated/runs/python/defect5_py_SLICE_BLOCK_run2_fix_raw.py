@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is not None:
        # infer based on element types inside the list: look for first non-None element
        inferred_elem_type = None
        for item in array:
            if item is not None:
                inferred_elem_type = type(item)
                break
        if inferred_elem_type is None:
            # array exists but all elements are None -> treat as object unless expected_type given
            inferred_type = object
        else:
            inferred_type = inferred_elem_type
    elif element is not None:
        inferred_type = type(element)
    else:
        # both array and element are None
        inferred_type = object

    new_list = ArrayUtils._copy_list_grow1(array, inferred_type)
    new_list[len(new_list) - 1] = element

    if expected_type is not None:
        # If inferred is object but expected_type is provided, allow if all non-None elements are instances of expected_type
        if inferred_type == object and expected_type != object:
            # check existing elements and the new element for compatibility
            incompatible_found = False
            # check array elements
            if array is not None:
                for item in array:
                    if item is not None and not isinstance(item, expected_type):
                        incompatible_found = True
                        break
            # check new element
            if not incompatible_found and element is not None and not isinstance(element, expected_type):
                incompatible_found = True
            if incompatible_found:
                raise TypeError(
                    f"Cannot cast object list to {expected_type.__name__} list "
                    f"(ClassCastException: [Ljava.lang.Object; cannot be cast to "
                    f"[Ljava.lang.{expected_type.__name__};)"
                )
        elif inferred_type is not object and not issubclass(inferred_type, expected_type):
            # inferred type is concrete but not compatible with expected_type
            raise TypeError(
                f"Cannot cast {inferred_type.__name__} list to {expected_type.__name__} list "
                f"(ClassCastException: [Ljava.lang.{inferred_type.__name__}; cannot be cast to "
                f"[Ljava.lang.{expected_type.__name__};)"
            )

    return new_list