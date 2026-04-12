@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is not None:
        inferred_type = type(array)
        if len(array) > 0:
            first_type = None
            for itm in array:
                if itm is not None:
                    first_type = type(itm)
                    break
            if first_type is None:
                inferred_type = object
            else:
                mixed = False
                for itm in array:
                    if itm is not None and type(itm) is not first_type:
                        mixed = True
                        break
                inferred_type = object if mixed else first_type
    elif element is not None:
        inferred_type = type(element)
    else:
        inferred_type = object

    new_list = ArrayUtils._copy_list_grow1(array, inferred_type)
    new_list[len(new_list) - 1] = element

    if expected_type is not None:
        if inferred_type == object and expected_type != object:
            raise TypeError(
                f"Cannot cast object list to {expected_type.__name__} list "
                f"(ClassCastException: [Ljava.lang.Object; cannot be cast to "
                f"[Ljava.lang.{expected_type.__name__};)"
            )

    return new_list