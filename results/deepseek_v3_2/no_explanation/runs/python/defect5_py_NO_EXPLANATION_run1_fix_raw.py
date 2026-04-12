    @staticmethod
    def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
        """
        Return a new list with `element` appended.

        This is a functional-style helper: the input list is not modified. If
        `array` is None, it is treated as an empty list.

        Args:
            array: Source list (may be None).
            element: Element to append.
            expected_type: Optional expected element type used to mirror Java-style
                component type checks in this translated code.
            
        Returns:
            A new list containing the original elements followed by `element`.
            
        Raises:
            TypeError: If `expected_type` is provided and the operation simulates a
                Java array cast failure.
        """
        if array is None:
            array = []
        new_list = array.copy()
        new_list.append(element)
        
        if expected_type is not None:
            # Simulate type checking: if array is empty, we cannot infer type.
            # In Java, if you try to cast an Object[] to a String[], you get ClassCastException.
            # Here we do a simple check: if the array is not empty, check the first element's type.
            # This is a simplified simulation.
            if array:
                first_type = type(array[0])
                if first_type != expected_type:
                    # Check if it's a subclass? For simplicity, we just compare.
                    # In Java, you cannot cast Object[] to String[] even if all elements are Strings.
                    # So we raise TypeError.
                    raise TypeError(
                        f"Cannot cast object list to {expected_type.__name__} list "
                        f"(ClassCastException: [Ljava.lang.Object; cannot be cast to "
                        f"[Ljava.lang.{expected_type.__name__};)"
                    )
        return new_list