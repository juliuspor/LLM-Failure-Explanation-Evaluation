@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is not None:
        # Try to infer a component type from existing elements: find first non-None element type
        inferred_component_type = None
        for item in array:
            if item is not None:
                inferred_component_type = type(item)
                break
        # If all elements are None, treat component type as object
        if inferred_component_type is None:
            inferred_component_type = object
    elif element is not None:
        inferred_component_type = type(element)
    else:
        inferred_component_type = object

    new_list = ArrayUtils._copy_list_grow1(array, inferred_component_type)
    new_list[len(new_list) - 1] = element

    # Only raise a simulated ClassCastException if the existing array implied a generic
    # object component type (i.e., array was provided and all elements were None or object)
    # and expected_type is provided and is more specific than object.
    if expected_type is not None:
        # Determine whether we should consider this a cast problem: if array was provided
        # and its inferred component type is object but expected_type is not object, then
        # previously this simulated a cast failure. However, if both array and element are None,
        # do not raise; simply return the new list containing None.
        if array is not None:
            # if array existed and had only None elements (component object), simulate failure
            if inferred_component_type == object and expected_type != object:
                raise TypeError(
                    f"Cannot cast object list to {expected_type.__name__} list "
                    f"(ClassCastException: [Ljava.lang.Object; cannot be cast to [Ljava.lang.{expected_type.__name__};)"
                )
    return new_list