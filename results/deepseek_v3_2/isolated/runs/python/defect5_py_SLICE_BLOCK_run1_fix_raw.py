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
            # Simulate Java's array type safety: if the inferred type is object (i.e., generic),
            # and the expected type is a specific type, we should only raise if the element
            # cannot be assigned to that type. However, Python is dynamically typed, so we
            # only raise if the element is not an instance of expected_type (if expected_type is a class).
            # But the original bug was raising incorrectly. We should check if the element is compatible.
            # However, the original code's condition was too strict. We'll adjust:
            # If expected_type is provided, we should check that the element is an instance of expected_type,
            # and also that all existing elements (if any) are instances of expected_type.
            # But to keep the fix simple and match the Java behavior, we can remove the condition that
            # raises when inferred_type == object and expected_type != object, because in Python we don't
            # have that restriction. Instead, we can just ignore the expected_type parameter for now,
            # or we can use it to validate the element's type.
            # Since the bug is about raising a TypeError incorrectly, we can simply remove the raise.
            # However, the expected_type parameter might be used for type checking in other contexts.
            # Let's change the condition: only raise if the element is not None and not an instance of expected_type.
            # But note: expected_type could be a built-in type like int, str, etc.
            # We'll implement a type check for the element only, because checking the whole array
            # would be expensive and not required for the fix.
            if element is not None and not isinstance(element, expected_type):
                raise TypeError(
                    f"Cannot add element of type {type(element).__name__} to array of type {expected_type.__name__}"
                )
        
        return new_list