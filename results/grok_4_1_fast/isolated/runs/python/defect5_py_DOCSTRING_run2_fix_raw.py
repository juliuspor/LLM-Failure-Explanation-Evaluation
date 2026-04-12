@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is None:
        new_list = []
    else:
        new_list = array.copy()
    new_list.append(element)
    
    if expected_type is not None:
        if array is not None:
            inferred_type = type(array[0]) if new_list else object
        elif element is not None:
            inferred_type = type(element)
        else:
            inferred_type = object
        
        if inferred_type != object and not issubclass(inferred_type, expected_type):
            raise TypeError(
                f"Cannot cast {inferred_type.__name__} list to {expected_type.__name__} list"
            )
    
    return new_list