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
            new_list = []
        elif isinstance(array, list):
            new_list = array.copy()
        else:
            # If array is not a list, treat it as a single-element list.
            # This maintains backward compatibility for non-list iterables?
            # However, the bug diagnosis indicates that passing a string leads to
            # unexpected decomposition. The function expects a list or None.
            # To fix, we should raise a TypeError or convert to list? 
            # The spec says: "array: Source list (may be None)." So it expects a list.
            # We'll raise a TypeError to enforce the contract.
            raise TypeError(f"array must be a list or None, got {type(array).__name__}")
        
        new_list.append(element)
        
        if expected_type is not None:
            # Simulate type checking: if array is None, inferred_type is object.
            # This is a simplified simulation.
            inferred_type = object
            if array is not None:
                # Try to infer the element type from the first element if list non-empty.
                if len(array) > 0:
                    inferred_type = type(array[0])
                else:
                    inferred_type = object
            if inferred_type == object and expected_type != object:
                raise TypeError(
                    f"Cannot cast object list to {expected_type.__name__} list "
                    f"(ClassCastException: [Ljava.lang.Object; cannot be cast to "
                    f"[Ljava.lang.{expected_type.__name__};)"
                )
        
        return new_list