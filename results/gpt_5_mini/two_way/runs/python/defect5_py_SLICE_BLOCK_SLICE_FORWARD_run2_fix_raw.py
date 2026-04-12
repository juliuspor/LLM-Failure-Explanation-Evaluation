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
        # If inferred_type is object (unknown element type), ensure all elements are instances of expected_type
        if inferred_type == object and expected_type != object:
            # Check existing elements in source array (if any) and the new element
            def all_match_expected():
                if array is not None:
                    for item in array:
                        if item is not None and not isinstance(item, expected_type):
                            return False
                # check the new element
                if element is not None and not isinstance(element, expected_type):
                    return False
                return True

            if not all_match_expected():
                raise TypeError(
                    f"Cannot cast object list to {expected_type.__name__} list "
                    f"(ClassCastException: [Ljava.lang.Object; cannot be cast to "
                    f"[Ljava.lang.{expected_type.__name__};)"
                )

    return new_list