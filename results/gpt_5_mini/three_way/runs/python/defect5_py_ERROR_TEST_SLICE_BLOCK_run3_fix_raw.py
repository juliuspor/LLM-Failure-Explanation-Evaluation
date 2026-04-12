@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is not None:
        inferred_type = type(array)
    elif element is not None:
        inferred_type = type(element)
    elif expected_type is not None:
        inferred_type = expected_type
    else:
        inferred_type = object

    new_list = ArrayUtils._copy_list_grow1(array, inferred_type)
    new_list[len(new_list) - 1] = element

    if expected_type is not None:
        # If inferred_type is a list/container type, we consider its element type unknown
        # Only raise if expected_type is incompatible with inferred_type when both are concrete types.
        try:
            inferred_is_object = (inferred_type is object)
            # If inferred_type is a type object representing the element type (from element or expected),
            # check compatibility. If inferred_type is a list type (e.g., type(list)), treat as unknown and allow.
            if not inferred_is_object:
                # If inferred_type is a type and expected_type is a type, ensure expected_type is subclass of inferred_type
                # or inferred_type is subclass of expected_type. For safety, only raise when neither is subclass of the other.
                if isinstance(inferred_type, type) and isinstance(expected_type, type):
                    if not (issubclass(expected_type, inferred_type) or issubclass(inferred_type, expected_type)):
                        raise TypeError(
                            f"Cannot cast object list to {expected_type.__name__} list "
                            f"(ClassCastException: [Ljava.lang.Object; cannot be cast to "
                            f"[Ljava.lang.{expected_type.__name__};)"
                        )
        except TypeError:
            # If issubclass gets a non-type, be conservative and allow the operation
            pass

    return new_list