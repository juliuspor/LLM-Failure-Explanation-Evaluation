@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is not None:
        # infer element type from existing elements, not the list container type
        inferred_element_type = None
        for item in array:
            if item is not None:
                inferred_element_type = type(item)
                break
        if inferred_element_type is None:
            # all elements are None or list empty
            if element is not None:
                inferred_element_type = type(element)
            else:
                inferred_element_type = object
    elif element is not None:
        inferred_element_type = type(element)
    else:
        inferred_element_type = object

    new_list = ArrayUtils._copy_list_grow1(array, inferred_element_type)
    new_list[len(new_list) - 1] = element

    if expected_type is not None:
        # Only raise if expected_type is more specific than object and incompatible
        if inferred_element_type is object:
            # if element is not None, check its compatibility
            if element is not None and not isinstance(element, expected_type):
                raise TypeError(
                    f"Cannot cast object list to {expected_type.__name__} list "
                    f"(ClassCastException: [Ljava.lang.Object; cannot be cast to "
                    f"[Ljava.lang.{expected_type.__name__};)"
                )
        else:
            # ensure inferred element type is compatible with expected_type
            if not issubclass(inferred_element_type, expected_type):
                # elements in array might still be instances of expected_type; check first non-None
                compatible = True
                if array is not None:
                    for item in array:
                        if item is not None and not isinstance(item, expected_type):
                            compatible = False
                            break
                if element is not None and not isinstance(element, expected_type):
                    compatible = False
                if not compatible:
                    raise TypeError(
                        f"Cannot cast {inferred_element_type.__name__} list to {expected_type.__name__} list "
                        f"(ClassCastException: [Ljava.lang.{inferred_element_type.__name__}; cannot be cast to "
                        f"[Ljava.lang.{expected_type.__name__};)"
                    )

    return new_list