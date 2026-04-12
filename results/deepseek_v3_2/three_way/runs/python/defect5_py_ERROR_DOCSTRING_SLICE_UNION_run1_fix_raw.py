    @staticmethod
    def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
        """
        Return a new list with element appended.
        """
        if array is not None:
            inferred_type = type(array[0]) if array else object
        elif element is not None:
            inferred_type = type(element)
        else:
            inferred_type = object
        
        new_list = ArrayUtils._copy_list_grow1(array, inferred_type)
        new_list[len(new_list) - 1] = element
        
        if expected_type is not None:
            if element is not None and not isinstance(element, expected_type):
                raise TypeError(
                    f"Cannot cast object to {expected_type.__name__} "
                    f"(ClassCastException: {type(element).__name__} cannot be cast to {expected_type.__name__})"
                )
        
        return new_list