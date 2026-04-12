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
        # Determine element type for type checking
        element_type = object
        if element is not None:
            element_type = type(element)
        # If array is not None, we could infer from its elements, but we don't have generic info.
        # For simulation, we treat the array's element type as object unless we can infer.
        # However, the bug diagnosis indicates that inferred_type should represent the element type,
        # not the container type. We'll set inferred_element_type to element_type when array is None,
        # and when array is not None, we try to infer from first element if exists, else object.
        inferred_element_type = object
        if array is not None and len(array) > 0:
            # Take type of first non-None element if possible
            for item in array:
                if item is not None:
                    inferred_element_type = type(item)
                    break
        elif array is not None and len(array) == 0:
            # Empty list: cannot infer, keep as object
            inferred_element_type = object
        else:
            # array is None
            inferred_element_type = element_type
        
        new_list = ArrayUtils._copy_list_grow1(array, inferred_element_type)
        new_list[len(new_list) - 1] = element
        
        if expected_type is not None:
            # Simulate Java array cast: if inferred element type is object and expected is not object,
            # raise TypeError.
            if inferred_element_type == object and expected_type != object:
                # Adjust Java class name: expected_type.__name__ might be 'str', but Java uses 'String'.
                # We'll keep as is for simplicity.
                raise TypeError(
                    f"Cannot cast object list to {expected_type.__name__} list "
                    f"(ClassCastException: [Ljava.lang.Object; cannot be cast to "
                    f"[Ljava.lang.{expected_type.__name__};)"
                )
        
        return new_list