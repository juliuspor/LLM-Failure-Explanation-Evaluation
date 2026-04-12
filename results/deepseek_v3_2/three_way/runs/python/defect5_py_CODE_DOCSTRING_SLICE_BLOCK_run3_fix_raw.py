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
            # Determine the element type of the array by checking the first element if exists
            if len(array) > 0:
                inferred_type = type(array[0])
            else:
                # Empty array: we cannot infer element type, treat as object
                inferred_type = object
        elif element is not None:
            inferred_type = type(element)
        else:
            inferred_type = object
        
        new_list = ArrayUtils._copy_list_grow1(array, inferred_type)
        new_list[len(new_list) - 1] = element
        
        if expected_type is not None:
            # Simulate Java array type mismatch: if inferred_type is object and expected_type is not object,
            # raise TypeError. Also, if inferred_type is not a subclass of expected_type, raise.
            # However, we only have the element type, not the array type. The original bug was comparing
            # inferred_type (which could be list or element type) to object. Now inferred_type is the element type.
            # We'll check if inferred_type is object (i.e., we couldn't determine a more specific type) and expected_type is not object.
            if inferred_type == object and expected_type != object:
                raise TypeError(
                    f"Cannot cast object list to {expected_type.__name__} list "
                    f"(ClassCastException: [Ljava.lang.Object; cannot be cast to "
                    f"[Ljava.lang.{expected_type.__name__};)"
                )
            # Additionally, if inferred_type is not a subclass of expected_type, we could raise,
            # but the original Java code likely only checks for object vs specific type.
            # We'll keep it simple: only raise when inferred_type is object and expected_type is not.
        
        return new_list