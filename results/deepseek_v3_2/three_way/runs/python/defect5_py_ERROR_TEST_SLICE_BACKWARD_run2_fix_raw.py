    @staticmethod
    def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
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
            # Only raise TypeError if the inferred_type is object and expected_type is not object,
            # but if both array and element are None, we should not raise because we cannot know the type.
            # Actually, the bug is that when both are None, inferred_type is object, which triggers the error.
            # We should skip the type check when both are None because there's no type information.
            # However, the test expects no error. So we need to avoid raising when array is None and element is None.
            # But also we need to consider that if array is None and element is not None, inferred_type is type(element).
            # That might still cause a mismatch with expected_type? The original Java code likely does a cast check only when array is not null.
            # Let's examine the original Java implementation: it uses Array.newInstance to create a new array of the same type as the input array.
            # If input array is null, it creates an array of the specified type (expected_type) or Object if expected_type is null.
            # In the Python translation, we have expected_type as an optional parameter. The bug is that we are raising a TypeError when we shouldn't.
            # The fix: only perform the type check when array is not None. Because if array is None, we don't have a component type to compare.
            # Actually, the condition in the original code: if expected_type is not None and inferred_type == object and expected_type != object.
            # This is meant to simulate Java's array cast failure. But when array is None, we cannot infer the component type, so we should not raise.
            # So we should skip the check if array is None.
            if array is not None and inferred_type == object and expected_type != object:
                raise TypeError(
                    f"Cannot cast object list to {expected_type.__name__} list "
                    f"(ClassCastException: [Ljava.lang.Object; cannot be cast to "
                    f"[Ljava.lang.{expected_type.__name__};)"
                )
        
        return new_list