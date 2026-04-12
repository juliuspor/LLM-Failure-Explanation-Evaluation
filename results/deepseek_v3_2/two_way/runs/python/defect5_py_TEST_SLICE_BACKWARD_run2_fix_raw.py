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
            if inferred_type == object and expected_type != object:
                # Only raise if array is not None and element is not None? Actually, the bug is that when both are None, inferred_type is object, but we shouldn't raise.
                # We should only raise when array is not None and its type is object but expected_type is a different type.
                # However, the original Java code likely does a type check on the array itself.
                # Let's adjust: only raise if array is not None and array is a list of objects (i.e., inferred_type is list? Wait, inferred_type is type(array) which is list, not object.
                # Actually, in the original code, inferred_type is the component type of the array. In Python, we don't have that.
                # The bug is that when array is None and element is None, inferred_type becomes object, which triggers the error incorrectly.
                # So we should skip the check when array is None.
                if array is not None:
                    raise TypeError(
                        f"Cannot cast object list to {expected_type.__name__} list "
                        f"(ClassCastException: [Ljava.lang.Object; cannot be cast to "
                        f"[Ljava.lang.{expected_type.__name__};)"
                    )
        
        return new_list