@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is not None and len(array) > 0:
        first_elem = array[0]
        element_type = type(first_elem) if first_elem is not None else object
    elif element is not None:
        element_type = type(element)
    else:
        element_type = object

    new_list = ArrayUtils._copy_list_grow1(array, element_type)
    new_list[len(new_list) - 1] = element

    if expected_type is not None:
        # If the inferred element type is object but expected is more specific, simulate cast failure
        if element_type == object and expected_type != object:
            raise TypeError(
                f"Cannot cast object list to {expected_type.__name__} list "
                f"(ClassCastException: [Ljava.lang.Object; cannot be cast to "
                f"[Ljava.lang.{expected_type.__name__};)"
            )
        # Also if inferred element type is different and not a subclass of expected_type, raise
        try:
            if element_type is not object and not issubclass(element_type, expected_type):
                raise TypeError(
                    f"Cannot cast {element_type.__name__} list to {expected_type.__name__} list "
                    f"(ClassCastException)"
                )
        except TypeError:
            # expected_type might not be a class for issubclass; ignore in that case
            pass

    return new_list