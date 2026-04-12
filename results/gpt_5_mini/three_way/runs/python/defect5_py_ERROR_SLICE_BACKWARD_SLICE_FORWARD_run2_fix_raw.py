@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is None:
        inferred_component_type = type(element) if element is not None else object
        new_list = [element]
    else:
        # Determine a sensible component type from existing elements
        inferred_component_type = None
        for itm in array:
            if itm is None:
                continue
            if inferred_component_type is None:
                inferred_component_type = type(itm)
            elif inferred_component_type != type(itm):
                inferred_component_type = object
                break
        if inferred_component_type is None:
            # All elements were None
            inferred_component_type = type(element) if element is not None else object
        new_list = array.copy()
        new_list.append(element)

    # Validate against expected_type if provided
    if expected_type is not None:
        # If inferred is object but expected_type is more specific, ensure element fits expected_type
        if inferred_component_type == object and expected_type != object:
            # If element is of expected type, allow. If array has any non-None element not of expected_type, reject.
            if element is not None and not isinstance(element, expected_type):
                raise TypeError(
                    f"Cannot cast object list to {expected_type.__name__} list (ClassCastException: [Ljava.lang.Object; cannot be cast to [Ljava.lang.{expected_type.__name__};)"
                )
            # check existing elements
            for itm in (array or []):
                if itm is not None and not isinstance(itm, expected_type):
                    raise TypeError(
                        f"Cannot cast object list to {expected_type.__name__} list (ClassCastException: [Ljava.lang.Object; cannot be cast to [Ljava.lang.{expected_type.__name__};)"
                    )
        else:
            # inferred is specific type: ensure it's compatible with expected_type
            if inferred_component_type is not object and expected_type is not object:
                if not issubclass(inferred_component_type, expected_type):
                    raise TypeError(
                        f"Cannot cast list of {inferred_component_type.__name__} to {expected_type.__name__}"
                    )

    return new_list