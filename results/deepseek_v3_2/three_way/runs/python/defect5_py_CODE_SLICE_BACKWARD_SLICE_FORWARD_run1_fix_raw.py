    @staticmethod
    def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
        if array is not None:
            if len(array) > 0:
                element_type = type(array[0])
            else:
                element_type = type(element) if element is not None else object
        elif element is not None:
            element_type = type(element)
        else:
            element_type = object
        
        new_list = ArrayUtils._copy_list_grow1(array, element_type)
        new_list[len(new_list) - 1] = element
        
        if expected_type is not None:
            if element_type == object and expected_type != object:
                raise TypeError(
                    f"Cannot cast object list to {expected_type.__name__} list "
                    f"(ClassCastException: [Ljava.lang.Object; cannot be cast to "
                    f"[Ljava.lang.{expected_type.__name__};)"
                )
        
        return new_list