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
            # Both array and element are None
            inferred_type = object
        
        new_list = ArrayUtils._copy_list_grow1(array, inferred_type)
        new_list[len(new_list) - 1] = element
        
        if expected_type is not None:
            if inferred_type == object and expected_type != object:
                # Only raise if we have a concrete array type that mismatches
                # If both array and element are None, we cannot infer a concrete type,
                # so we should not raise a TypeError.
                # However, we need to check if array is not None and its type is object.
                # Actually, the condition above is too broad. We should only raise when
                # array is not None and its type is object (i.e., a list of objects)
                # but expected_type is a different type.
                # But inferred_type is the type of the array (if array is not None) or type(element).
                # If array is None, inferred_type is either type(element) or object.
                # If array is None and element is None, inferred_type is object.
                # In that case, we should not raise because there is no concrete array.
                # So we need to know whether we had an actual array (non-None) that is of object type.
                # Let's adjust: only raise if array is not None and the array's type is object.
                # However, we don't have the array's type stored separately.
                # We can check if array is not None and all elements are objects? Not feasible.
                # Instead, we can change the logic: if array is None, we treat it as an empty list,
                # and there is no type mismatch because we can create a list of any type.
                # So we should skip the type check when array is None.
                if array is not None:
                    raise TypeError(
                        f"Cannot cast object list to {expected_type.__name__} list "
                        f"(ClassCastException: [Ljava.lang.Object; cannot be cast to "
                        f"[Ljava.lang.{expected_type.__name__};)"
                    )
        
        return new_list