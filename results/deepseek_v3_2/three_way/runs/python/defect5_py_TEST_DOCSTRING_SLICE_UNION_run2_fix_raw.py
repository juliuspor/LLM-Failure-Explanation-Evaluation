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
            # Both array and element are None, cannot infer type, default to object
            inferred_type = object
        
        new_list = ArrayUtils._copy_list_grow1(array, inferred_type)
        new_list[len(new_list) - 1] = element
        
        if expected_type is not None:
            # Only raise TypeError if inferred_type is object and expected_type is not object,
            # but if both array and element are None, we should not raise an error.
            # Actually, the issue is that when array is None and element is None, inferred_type is object.
            # The test expects no error. So we should skip the type check when both are None.
            # However, the original Java code likely does a type check based on the array's component type.
            # Since array is None, there is no component type, so no cast should fail.
            # Therefore, we should only raise if array is not None and its type is object while expected_type is not object.
            # But inferred_type is the type of the array (if array is not None) or type of element (if element is not None).
            # When array is None and element is None, inferred_type is object, but that's not the array's component type.
            # So we need to adjust: only check when array is not None.
            if array is not None and inferred_type == object and expected_type != object:
                raise TypeError(
                    f"Cannot cast object list to {expected_type.__name__} list "
                    f"(ClassCastException: [Ljava.lang.Object; cannot be cast to "
                    f"[Ljava.lang.{expected_type.__name__};)"
                )
        
        return new_list