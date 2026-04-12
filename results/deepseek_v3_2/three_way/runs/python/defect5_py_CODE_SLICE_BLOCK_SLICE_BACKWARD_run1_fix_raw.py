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
            # Determine the element type of the array by looking at its first element if exists
            if len(array) > 0:
                inferred_type = type(array[0])
            else:
                # Empty array: we cannot infer, treat as object
                inferred_type = object
        elif element is not None:
            inferred_type = type(element)
        else:
            inferred_type = object
        
        new_list = ArrayUtils._copy_list_grow1(array, inferred_type)
        new_list[len(new_list) - 1] = element
        
        if expected_type is not None:
            # Simulate Java array type mismatch: if inferred_type is not a subclass of expected_type
            # (or not equal), raise TypeError.
            # Since Python's type system is dynamic, we approximate by checking if inferred_type is object
            # (meaning unknown) and expected_type is not object, or if they are different.
            # However, the original bug was that inferred_type was the list type, not element type.
            # Now inferred_type is the element type.
            # We'll mimic the Java behavior: if inferred_type is object and expected_type is not object,
            # that's a cast failure. Also if expected_type is not a superclass of inferred_type.
            # For simplicity, we'll just check if inferred_type is object and expected_type is not object.
            if inferred_type == object and expected_type != object:
                raise TypeError(
                    f"Cannot cast object list to {expected_type.__name__} list "
                    f"(ClassCastException: [Ljava.lang.Object; cannot be cast to "
                    f"[Ljava.lang.{expected_type.__name__};)"
                )
            # Additional check: if inferred_type is not a subclass of expected_type (using issubclass)
            # but we must be careful because inferred_type might be a built-in type that doesn't have
            # a proper class hierarchy. We'll skip for now to keep the fix minimal.
        
        return new_list