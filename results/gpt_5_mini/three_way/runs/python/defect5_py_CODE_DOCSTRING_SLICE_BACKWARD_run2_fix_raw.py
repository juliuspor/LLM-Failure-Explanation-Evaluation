@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is not None:
        # Infer element type from first non-None element in array
        inferred_element_type = None
        for item in array:
            if item is not None:
                inferred_element_type = type(item)
                break
        # If all elements are None, and element provided, use its type, else object
        if inferred_element_type is None:
            if element is not None:
                inferred_element_type = type(element)
            else:
                inferred_element_type = object
    elif element is not None:
        inferred_element_type = type(element)
    else:
        inferred_element_type = object

    # Validate expected_type compatibility early
    if expected_type is not None:
        # If expected_type is not object and inferred is object but element is not None,
        # check the element's type
        if inferred_element_type == object:
            if element is not None and not isinstance(element, expected_type):
                raise TypeError(
                    f"Cannot cast object list to {expected_type.__name__} list "
                    f"(ClassCastException: [Ljava.lang.Object; cannot be cast to "
                    f"[Ljava.lang.{expected_type.__name__};)"
                )
        else:
            # If we have a concrete inferred element type, ensure it's compatible with expected_type
            # Allow subclassing
            try:
                is_compatible = issubclass(inferred_element_type, expected_type)
            except TypeError:
                is_compatible = False
            if not is_compatible:
                # If element itself is instance of expected_type, allow (covers generics)
                if element is None or not isinstance(element, expected_type):
                    raise TypeError(
                        f"Cannot cast {inferred_element_type.__name__} list to {expected_type.__name__} list "
                        f"(ClassCastException: [Ljava.lang.{inferred_element_type.__name__}; cannot be cast to "
                        f"[Ljava.lang.{expected_type.__name__};)"
                    )

    new_list = ArrayUtils._copy_list_grow1(array, inferred_element_type)
    new_list[len(new_list) - 1] = element
    return new_list