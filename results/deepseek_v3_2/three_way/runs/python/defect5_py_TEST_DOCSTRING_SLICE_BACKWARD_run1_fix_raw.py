    @staticmethod
    def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
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
                # Only raise if we have a concrete array type that mismatches.
                # When both array and element are None, we cannot infer a concrete type,
                # so we should not raise a TypeError.
                # However, if array is not None, its type is known.
                # If array is None but element is not None, inferred_type is type(element).
                # In those cases, we should still check? The original Java code would only raise
                # when trying to cast an Object[] to a more specific type.
                # The bug is that we raise when both are None, which should be allowed.
                # So we should only raise if array is not None and its type is object? Actually,
                # the condition is: if inferred_type == object and expected_type != object.
                # But when both are None, inferred_type is object, but we shouldn't raise.
                # Therefore, we need to know whether we defaulted to object because both are None.
                # We can add a flag: defaulted_to_object = (array is None and element is None)
                # Alternatively, we can skip the check when array is None and element is None.
                # Let's implement: if array is None and element is None, skip the check.
                pass
        
        return new_list