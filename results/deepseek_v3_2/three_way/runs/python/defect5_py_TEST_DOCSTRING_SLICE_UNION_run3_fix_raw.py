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
            inferred_type = type(array)
        elif element is not None:
            inferred_type = type(element)
        else:
            # Both array and element are None: we cannot infer a type.
            # If expected_type is provided, we should use that for the type check.
            # Otherwise, default to object.
            inferred_type = object
        
        new_list = ArrayUtils._copy_list_grow1(array, inferred_type)
        new_list[len(new_list) - 1] = element
        
        if expected_type is not None:
            # If inferred_type is object (because both array and element are None),
            # we should not raise a TypeError because there is no actual type conflict.
            # Only raise if inferred_type is not object and expected_type != inferred_type.
            # However, inferred_type could be a list type (e.g., list), not the element type.
            # The original Java code checks component type of the array.
            # In this Python simulation, we only raise when inferred_type is object
            # and expected_type is not object? Actually, the bug is that we raise
            # when both are None and expected_type is not object.
            # We should avoid raising when there is no actual type information.
            # So we can skip the check if inferred_type is object and both inputs are None.
            # But we also need to consider the case where array is None but element is not None:
            # then inferred_type is type(element). That's fine.
            # The problematic case is when array is None and element is None.
            # In that case, we should not raise regardless of expected_type.
            # So we can check: if array is None and element is None, skip the type check.
            if not (array is None and element is None):
                if inferred_type == object and expected_type != object:
                    raise TypeError(
                        f"Cannot cast object list to {expected_type.__name__} list "
                        f"(ClassCastException: [Ljava.lang.Object; cannot be cast to "
                        f"[Ljava.lang.{expected_type.__name__};)"
                    )
        
        return new_list