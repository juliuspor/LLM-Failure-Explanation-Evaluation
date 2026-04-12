    @staticmethod
    def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
        """
        Return a new list with `element` appended.

        This is a helper that does not modify the input. If `array` is None, it's treated as empty.

        Args:
            array: Source list (may be None).
            element: Element to append.
            expected_type: Optional expected element type for type-check simulation.
        
        Returns:
            A new list with the element added.
        """
        if array is not None and len(array) > 0:
            inferred_type = type(array[0])
        elif element is not None:
            inferred_type = type(element)
        else:
            inferred_type = object
        
        new_list = ArrayUtils._copy_list_grow1(array, inferred_type)
        new_list[-1] = element
        
        if expected_type is not None:
            if inferred_type == object and expected_type != object:
                raise TypeError(
                    f"Casting object list to {expected_type.__name__} is not allowed "
                    f"(ClassCastException: [Ljava.lang.Object; cannot be cast to "
                    f"[Ljava.lang.{expected_type.__name__};)"
                )
        
        return new_list