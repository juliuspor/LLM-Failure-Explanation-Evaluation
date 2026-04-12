@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is not None:
        non_none_elements = [x for x in array if x is not None]
        if non_none_elements:
            inferred_type = type(non_none_elements[0])
            for x in non_none_elements[1:]:
                if type(x) != inferred_type:
                    inferred_type = object
                    break
        else:
            inferred_type = object
    elif element is not None:
        inferred_type = type(element)
    else:
        inferred_type = object

    new_list = ArrayUtils._copy_list_grow1(array, inferred_type)
    new_list[len(new_list) - 1] = element

    if expected_type is not None:
        if inferred_type == object and expected_type != object:
            elements_to_check = []
            if array is not None:
                elements_to_check = [x for x in array if x is not None]
            if element is not None:
                elements_to_check.append(element)
            for idx, el in enumerate(elements_to_check):
                if not isinstance(el, expected_type):
                    raise TypeError(
                        f"Cannot cast object list to {expected_type.__name__} list "
                        f"(ClassCastException: [Ljava.lang.Object; cannot be cast to "
                        f"[Ljava.lang.{expected_type.__name__};)"
                    )
    return new_list