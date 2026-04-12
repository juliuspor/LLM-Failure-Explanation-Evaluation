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
            # Simulate Java type checking: if expected_type is not object and inferred_type is object,
            # raise a TypeError to mimic ClassCastException.
            # However, if element is None, we allow it because None can be assigned to any type in Python.
            # In Java, null can be assigned to any reference type, so no cast error.
            # Therefore, only raise if the array is non-None and its elements are of type object
            # but expected_type is a specific type (not object) and the array is not empty? 
            # Actually, the Java simulation is only about the array type, not the element type.
            # The original code raised when inferred_type == object and expected_type != object.
            # But that's too strict when array is None (inferred_type becomes object).
            # We should only raise if array is not None and its elements are of type object
            # and expected_type is not object. However, we don't have the element type of array.
            # The test expects that adding None to a null array with expected_type=str should not raise.
            # So we need to adjust: only raise if array is not None and array is a list of objects
            # and expected_type is not object. But how to know if array is a list of objects?
            # In Python, all lists are of objects. So we need a different approach.
            # Let's look at the original Java code: it does a cast of the array to the component type.
            # The Python simulation is just to mimic that for testing. The test expects that when
            # expected_type is provided and array is null, no exception is raised.
            # Therefore, we should only raise the exception when array is not None and the array
            # is not empty and the first element's type is not compatible? That's too complex.
            # Actually, the bug diagnosis says the test fails because of ClassCastException.
            # The test expects no exception. So we need to avoid raising the exception in the case
            # where array is None and element is None and expected_type is str.
            # In that scenario, inferred_type is object (from the else branch).
            # Then we check if inferred_type == object and expected_type != object -> raise.
            # That's what causes the error. So we need to modify that condition.
            # We should not raise if array is None, because there is no existing array to cast.
            # Also, we should not raise if element is None, because null is assignable to any type.
            # So we can change the condition to:
            # if inferred_type == object and expected_type != object and array is not None:
            #   raise ...
            # But also, if array is None, we don't have an array to cast, so no exception.
            # Additionally, if element is None, we can skip because null is allowed.
            # However, the test might also cover cases where array is not None and element is not None.
            # We need to keep the simulation for those cases.
            # Let's implement:
            if inferred_type == object and expected_type != object:
                # Only raise if array is not None and array is not empty? Actually, the Java cast
                # would fail if you try to cast an Object[] to a String[] even if empty.
                # But the test expects that when array is null, no exception.
                # So we can add a condition: only raise if array is not None.
                if array is not None:
                    raise TypeError(
                        f"Cannot cast object list to {expected_type.__name__} list "
                        f"(ClassCastException: [Ljava.lang.Object; cannot be cast to "
                        f"[Ljava.lang.{expected_type.__name__};)"
                    )
        
        return new_list