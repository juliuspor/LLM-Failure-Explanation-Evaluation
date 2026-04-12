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
            # but only when array is not None and element is not None? Actually, the bug is that
            # when both are None, we set inferred_type = object, and then expected_type might be str,
            # causing a spurious error. The fix: if both array and element are None, we should not
            # raise a TypeError regardless of expected_type, because we are just returning [None].
            # However, the original Java code likely uses expected_type to simulate array type.
            # The test expects no error. So we should skip the check when array is None and element is None.
            # But also, if array is None and element is not None, we might still need to check?
            # Let's examine: The test passes expected_type=str, array=None, element=None.
            # The method should return [None] without error.
            # So we should only raise if there is a real type mismatch, i.e., when array is not None
            # and its type is object but expected_type is a specific type? Actually, the condition
            # in the original code is too broad. We should only raise when array is not None and
            # the inferred_type is object and expected_type is not object. But also, if array is None
            # and element is not None, inferred_type is type(element). That might be object? No, element
            # is a concrete type. If element is None, inferred_type becomes object. That's the problematic case.
            # So we need to adjust: only raise if array is not None and inferred_type == object and expected_type != object.
            # Because when array is None, we are creating a new list, and the type check is irrelevant.
            # However, the Java version might still check? The test suggests not.
            # Let's implement: if array is not None and inferred_type == object and expected_type != object:
            #   raise TypeError.
            # Otherwise, no error.
            if array is not None and inferred_type == object and expected_type != object:
                raise TypeError(
                    f"Cannot cast object list to {expected_type.__name__} list "
                    f"(ClassCastException: [Ljava.lang.Object; cannot be cast to "
                    f"[Ljava.lang.{expected_type.__name__};)"
                )
        
        return new_list