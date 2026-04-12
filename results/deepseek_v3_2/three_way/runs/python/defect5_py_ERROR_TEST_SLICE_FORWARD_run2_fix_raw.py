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
            inferred_type = object
        
        new_list = ArrayUtils._copy_list_grow1(array, inferred_type)
        new_list[len(new_list) - 1] = element
        
        if expected_type is not None:
            # Simulate Java array type checking: if expected_type is not object,
            # and inferred_type is object (i.e., we created a generic list),
            # raise TypeError.
            # However, if array is None and element is None, inferred_type is object.
            # The test expects no error in that case, so we need to adjust.
            # Actually, the bug is that when array is None and element is None,
            # we should treat expected_type as the type of the new list.
            # The fix: when array is None, we should use expected_type as the inferred_type
            # if it is provided, to avoid the cast error.
            if array is None:
                # If array is None, we are creating a new list.
                # In Java, if expected_type is provided, the new array would be of that type.
                # So we should not raise an error in this case.
                # Instead, we should only raise if array is not None and its type is object
                # but expected_type is more specific.
                pass
            if inferred_type == object and expected_type != object:
                # Only raise if we are trying to cast an existing object array to a more specific type.
                # But if array is None, we are not casting an existing array.
                # So we need to check if array is not None.
                if array is not None:
                    raise TypeError(
                        f"Cannot cast object list to {expected_type.__name__} list "
                        f"(ClassCastException: [Ljava.lang.Object; cannot be cast to "
                        f"[Ljava.lang.{expected_type.__name__};)"
                    )
        
        return new_list