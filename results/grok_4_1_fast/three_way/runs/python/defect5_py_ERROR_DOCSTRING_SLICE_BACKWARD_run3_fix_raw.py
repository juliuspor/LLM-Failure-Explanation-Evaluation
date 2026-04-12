@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is not None:
        inferred_type = type(array[0]) if array else object
    elif element is not None:
        inferred_type = type(element)
    else:
        inferred_type = object
    
    new_list = ArrayUtils._copy_list_grow1(array, None)
    new_list[len(new_list) - 1] = element
    
    if expected_type is not None:
        needs_cast = inferred_type != expected_type
        if needs_cast:
            # Simulate Java array cast check
            if inferred_type == object or issubclass(expected_type, inferred_type):
                # Check if elements actually match expected_type
                for item in new_list:
                    if item is not None and not isinstance(item, expected_type):
                        raise TypeError(
                            f"Cannot cast object list to {expected_type.__name__} list "
                            f"(ClassCastException: [Ljava.lang.Object; cannot be cast to "
                            f"[Ljava.lang.{expected_type.__name__};)"
                        )
            else:
                raise TypeError(
                    f"Cannot cast {inferred_type.__name__} list to {expected_type.__name__} list "
                    f"(ClassCastException: [L{inferred_type.__name__}; cannot be cast to "
                    f"[L{expected_type.__name__};)"
                )
    
    return new_list
