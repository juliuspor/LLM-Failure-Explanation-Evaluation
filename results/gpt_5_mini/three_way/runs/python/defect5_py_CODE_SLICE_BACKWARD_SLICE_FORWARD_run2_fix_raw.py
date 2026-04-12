@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is not None:
        # Infer component type from existing elements: find first non-None element
        inferred_component_type = None
        for item in array:
            if item is not None:
                inferred_component_type = type(item)
                break
        if inferred_component_type is None:
            # all elements are None -> unknown component type
            inferred_component_type = object
    elif element is not None:
        inferred_component_type = type(element)
    else:
        inferred_component_type = object

    new_list = ArrayUtils._copy_list_grow1(array, inferred_component_type)
    new_list[len(new_list) - 1] = element

    if expected_type is not None:
        # If component type is unknown (object) but expected_type is specific, simulate cast failure
        if inferred_component_type is object and expected_type is not object:
            raise TypeError(
                f"Cannot cast object list to {expected_type.__name__} list "
                f"(ClassCastException: [Ljava.lang.Object; cannot be cast to "
                f"[Ljava.lang.{expected_type.__name__};)"
            )
        # If we do know a concrete component type, ensure it's compatible with expected_type
        if inferred_component_type is not object and expected_type is not object:
            # If element types are incompatible (not subclass), raise
            # Use issubclass for type objects, but guard if inferred_component_type isn't a class
            try:
                if not issubclass(inferred_component_type, expected_type):
                    raise TypeError(
                        f"Cannot cast {inferred_component_type.__name__} list to {expected_type.__name__} list"
                    )
            except TypeError:
                # issubclass raised because inferred_component_type is not a class
                pass

    return new_list