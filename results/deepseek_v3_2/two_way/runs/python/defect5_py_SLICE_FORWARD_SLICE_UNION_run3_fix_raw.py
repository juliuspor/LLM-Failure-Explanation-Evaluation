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
            # Both array and element are None, we cannot infer a type.
            # Use a special sentinel to indicate unknown type.
            inferred_type = None
        
        new_list = ArrayUtils._copy_list_grow1(array, inferred_type)
        new_list[len(new_list) - 1] = element
        
        if expected_type is not None:
            # If inferred_type is None (unknown), we cannot perform type check.
            # But we can still raise if expected_type is not object? 
            # The original Java code would have a component type for the array.
            # Since we are simulating, we only raise when inferred_type is exactly object
            # and expected_type is not object. However, we need to adjust because
            # inferred_type could be a subclass of object. Actually, the condition
            # should be: if inferred_type is not None and inferred_type != expected_type?
            # But the original bug is about using object as sentinel. Let's keep the
            # original logic but fix the sentinel: we should not treat object as sentinel.
            # Instead, we can treat None as sentinel for unknown type.
            # The original condition was checking if inferred_type == object and expected_type != object.
            # That condition is meant to simulate a Java ClassCastException when trying to cast
            # an Object[] to a more specific array type. In Python, we can't replicate exactly.
            # We'll keep the same logic but with a clearer sentinel.
            # If inferred_type is None (unknown), we skip the check.
            if inferred_type is not None and inferred_type == object and expected_type != object:
                raise TypeError(
                    f"Cannot cast object list to {expected_type.__name__} list "
                    f"(ClassCastException: [Ljava.lang.Object; cannot be cast to "
                    f"[Ljava.lang.{expected_type.__name__};)"
                )
        
        return new_list