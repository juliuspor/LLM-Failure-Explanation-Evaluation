@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is not None:
        # Infer from first non-None element or default to object
        inferred_type = object
        for item in array:
            if item is not None:
                inferred_type = type(item)
                break
    elif element is not None:
        inferred_type = type(element)
    else:
        inferred_type = object
    
    new_list = ArrayUtils._copy_list_grow1(array, inferred_type)
    new_list[len(new_list) - 1] = element
    
    if expected_type is not None and inferred_type != expected_type:
        raise TypeError(
            f"Cannot cast {inferred_type.__name__} list to {expected_type.__name__} list "
            f"(ClassCastException: [L{inferred_type.__module__.split('.')[-1].title()}; cannot be cast to "
            f"[L{expected_type.__module__.split('.')[-1].title()};)"
        )
    
    return new_list
