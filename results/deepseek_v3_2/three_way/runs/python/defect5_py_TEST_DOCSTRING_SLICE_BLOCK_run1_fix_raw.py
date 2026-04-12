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
                # Only raise if the array is non-None and its type is object but expected_type is not object.
                # If array is None and element is None, inferred_type is object, but we should allow it.
                # So we need to check if the array is actually a list of objects (i.e., array is not None and its type is list).
                # However, type(array) when array is a list returns list, not object.
                # Actually, inferred_type is set to type(array) which is list, or type(element) which could be NoneType.
                # Wait: In the bug scenario, array is None, element is None, so inferred_type becomes object.
                # That's the problem. We should not raise when array is None and element is None.
                # So we can add a condition: if array is None and element is None, skip the check.
                # But also if array is None and element is not None, inferred_type is type(element).
                # So we can check if array is None: then we are creating a new list, so no cast issue.
                # Therefore, we should only raise if array is not None and inferred_type == object and expected_type != object.
                # However, inferred_type is type(array) which is list, not object. Wait, object is a class.
                # In the code, inferred_type is set to object only when both array is None and element is None.
                # That's the only case where inferred_type == object.
                # So we can simply skip the check when array is None.
                if array is not None:
                    raise TypeError(
                        f"Cannot cast object list to {expected_type.__name__} list "
                        f"(ClassCastException: [Ljava.lang.Object; cannot be cast to "
                        f"[Ljava.lang.{expected_type.__name__};)"
                    )
        
        return new_list