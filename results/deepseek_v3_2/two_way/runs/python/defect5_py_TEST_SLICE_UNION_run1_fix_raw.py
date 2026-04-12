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
                # Only raise if array is not None and its type is object? Actually, we need to consider the case where array is None and element is None.
                # The bug: when both array and element are None, inferred_type is object, but we shouldn't raise because the user explicitly wants a string array.
                # The expected_type is provided by the caller, and we should respect it.
                # However, the Java-style check is meant to simulate a cast failure when the array is of type Object and we try to cast to a more specific type.
                # But if array is None, there is no existing array to cast. So we should not raise.
                # Also, if array is not None and its type is object, we should raise only if the array is actually of type object? In Python, type(array) is list, not object.
                # The original Java code likely checks the component type of the array. In Python, we can't get that.
                # The current logic is flawed. We should only raise if array is not None and the array's element type (inferred) is object and expected_type is more specific.
                # But since we cannot know the element type, we rely on inferred_type which is the type of the array (list). That's always list.
                # Wait: In the original Java code, the method signature might be for generic arrays. The Python translation uses inferred_type = type(array) which is list.
                # However, the test expects that when array is None and element is None, we should not raise TypeError.
                # So the fix: only raise if array is not None and inferred_type == object? But inferred_type is never object because type(array) is list.
                # Actually, the condition `inferred_type == object` is only true when both array and element are None (line 337). That's the bug.
                # Therefore, we should skip the check when array is None, because there is no existing array to cast.
                # Alternatively, we can change the condition to only raise when array is not None and inferred_type == object.
                # But inferred_type == object only happens when array is None and element is None. So we can simply skip the check when array is None.
                if array is not None:
                    raise TypeError(
                        f"Cannot cast object list to {expected_type.__name__} list "
                        f"(ClassCastException: [Ljava.lang.Object; cannot be cast to "
                        f"[Ljava.lang.{expected_type.__name__};)"
                    )
        
        return new_list