@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is not None and len(array) > 0:
        # infer element type from existing elements if they are uniform
        first_type = type(array[0])
        uniform = True
        for item in array:
            if item is not None and type(item) != first_type:
                uniform = False
                break
        inferred_type = first_type if uniform else object
    elif element is not None:
        inferred_type = type(element)
    else:
        inferred_type = object

    new_list = ArrayUtils._copy_list_grow1(array, inferred_type)
    new_list[len(new_list) - 1] = element

    if expected_type is not None:
        # Validate compatibility: allow None, or element instance, or existing array element types compatible
        compatible = True
        if element is not None and not isinstance(element, expected_type):
            compatible = False
        if array is not None and len(array) > 0:
            for item in array:
                if item is not None and not isinstance(item, expected_type):
                    compatible = False
                    break
        if not compatible:
            raise TypeError(
                f"Cannot cast list elements to {expected_type.__name__} list "
                f"(ClassCastException: [Ljava.lang.Object; cannot be cast to [Ljava.lang.{expected_type.__name__};)"
            )

    return new_list