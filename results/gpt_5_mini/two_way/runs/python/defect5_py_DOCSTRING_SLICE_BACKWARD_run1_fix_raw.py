@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is not None:
        # Infer element/component type by looking for the first non-None element
        inferred_type = None
        for item in array:
            if item is not None:
                inferred_type = type(item)
                break
    elif element is not None:
        inferred_type = type(element)
    else:
        # Both array and element are None -> unknown component type
        inferred_type = None

    new_list = ArrayUtils._copy_list_grow1(array, inferred_type)
    new_list[len(new_list) - 1] = element

    if expected_type is not None:
        # If we have no information about inferred_type (None), don't raise
        # If inferred_type is object (very generic), allow unless expected_type is more specific and incompatible
        if inferred_type is not None:
            # If inferred_type is not a subclass/instance of expected_type, raise
            try:
                if not issubclass(inferred_type, expected_type):
                    raise TypeError(
                        f"Cannot cast {inferred_type.__name__} list to {expected_type.__name__} list "
                        f"(ClassCastException: [Ljava.lang.{inferred_type.__name__}; cannot be cast to "
                        f"[Ljava.lang.{expected_type.__name__};)"
                    )
            except TypeError:
                # issubclass can raise TypeError if expected_type is not a class
                if inferred_type is not None and not isinstance(None, expected_type):
                    raise TypeError(
                        f"Cannot cast {inferred_type.__name__} list to {expected_type.__name__} list"
                    )

    return new_list