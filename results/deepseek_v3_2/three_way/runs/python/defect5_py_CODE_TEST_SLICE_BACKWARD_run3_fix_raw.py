    @staticmethod
    def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
        if array is not None:
            new_list = array.copy()
            new_list.append(element)
        else:
            new_list = [element]
        
        if expected_type is not None:
            # Simulate Java type mismatch error for compatibility
            raise TypeError(
                f"Cannot cast object list to {expected_type.__name__} list "
                f"(ClassCastException: [Ljava.lang.Object; cannot be cast to "
                f"[L{expected_type.__name__};)"
            )
        return new_list