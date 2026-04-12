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
        if array is not None:
            # Determine element type from the first element if array is non-empty
            if len(array) > 0:
                inferred_type = type(array[0])
            else:
                # Empty array: use element's type if element is not None, else object
                if element is not None:
                    inferred_type = type(element)
                else:
                    inferred_type = object
        else:
            # array is None: use element's type if element is not None, else object
            if element is not None:
                inferred_type = type(element)
            else:
                inferred_type = object
        
        new_list = ArrayUtils._copy_list_grow1(array, inferred_type)
        new_list[len(new_list) - 1] = element
        
        if expected_type is not None:
            # Simulate Java array type mismatch: if inferred_type is not compatible with expected_type
            # For simplicity, we treat object as generic and any other type as specific.
            # If inferred_type is object and expected_type is not object, raise.
            # Also, if inferred_type is not object and expected_type is not object and they differ, raise.
            # This is a simplified simulation.
            if inferred_type == object and expected_type != object:
                raise TypeError(
                    f"Cannot cast object list to {expected_type.__name__} list "
                    f"(ClassCastException: [Ljava.lang.Object; cannot be cast to "
                    f"[Ljava.lang.{expected_type.__name__};)"
                )
            # Additional check: if inferred_type is not object and expected_type is not object and they differ
            if inferred_type != object and expected_type != object and inferred_type != expected_type:
                raise TypeError(
                    f"Cannot cast {inferred_type.__name__} list to {expected_type.__name__} list "
                    f"(ClassCastException: [Ljava.lang.{inferred_type.__name__}; cannot be cast to "
                    f"[Ljava.lang.{expected_type.__name__};)"
                )
        
        return new_list