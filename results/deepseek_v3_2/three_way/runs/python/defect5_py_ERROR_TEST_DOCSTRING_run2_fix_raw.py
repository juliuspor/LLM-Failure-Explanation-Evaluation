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
                # Only raise if array is not None and element is not None? Actually, we need to mimic Java behavior.
                # The test expects that when array is None and element is None, we should not raise.
                # So we should only raise when array is not None and its type is object and expected_type is not object.
                # But also when array is None and element is not None, inferred_type is type(element).
                # If element is None, inferred_type is object, but we should not raise because we are adding None to None.
                # The test case: add(None, None, expected_type=str) should return [None] without error.
                # So we need to check if array is None and element is None, then skip the error.
                # Actually, the condition should be: if array is not None and inferred_type == object and expected_type != object:
                # But also if array is None and element is not None, inferred_type is type(element). That might not be object.
                # However, the Java simulation is about casting the array type. If array is None, there is no existing array to cast.
                # So we should only raise when array is not None and its inferred_type (which is type(array)) is object and expected_type is not object.
                # But note: type(array) is List[T] not the element type. We need to simulate the element type.
                # In the original code, inferred_type is set to type(array) which is list, not the element type.
                # That's wrong. We need to infer the element type, not the list type.
                # Actually, the Java version checks the component type of the array. In Python, we don't have that.
                # The bug is that the type check is too strict and triggers incorrectly for None inputs.
                # The test expects that when both array and element are None, no error is raised.
                # So we can adjust the condition: only raise if array is not None and element is not None? Not exactly.
                # Let's think: The error is about casting an Object[] to String[]. If the array is null (None), there is no array to cast.
                # So we should only raise when array is not None. Because if array is None, we are creating a new list, not casting.
                # Therefore, we can change the condition to: if array is not None and inferred_type == object and expected_type != object:
                # But inferred_type is type(array) which is list, not object. So we need a different approach.
                # Actually, the original code uses inferred_type == object as a proxy for Object[]. That's not accurate.
                # Since we cannot know the element type of a list in Python, we rely on the element's type when array is None.
                # The test case: add(None, None, expected_type=str) -> inferred_type = object (because element is None).
                # Then condition inferred_type == object and expected_type != object is true, so it raises.
                # To fix, we should skip the type check when array is None and element is None.
                # Alternatively, we can skip the type check entirely when array is None, because there is no existing array to cast.
                # That seems logical: the type check is only relevant when we have an existing array that we are "growing".
                # If array is None, we are creating a new list, and the expected_type is just a hint, but we don't need to enforce.
                # The docstring says: "If expected_type is provided and the operation simulates a Java array cast failure."
                # The simulation should only happen when we are trying to cast an existing array.
                # So we can change the condition to: if array is not None and expected_type is not None:
                # But we still need to infer the element type of the existing array? We don't have that.
                # The original code uses inferred_type == object as a proxy for Object[]. That's a simplification.
                # We'll keep that simplification but only apply it when array is not None.
                # So: if array is not None and expected_type is not None:
                #   if inferred_type == object and expected_type != object:
                #        raise ...
                # But inferred_type is type(array) which is list, not object. Wait, we set inferred_type to type(array) when array is not None.
                # That's wrong. We should set inferred_type to the element type? We can't.
                # Actually, the Java simulation is about the component type of the array. In Python, we don't have that.
                # The test expects that when array is None and element is None, no error.
                # So we can simply skip the type check when array is None.
                # Let's do that.
                if array is not None:
                    # We need to decide what inferred_type should be for the array's element type.
                    # Since we can't, we'll assume that if array is not empty, we can look at the first element.
                    # But that's not safe. The original code used inferred_type = type(array) which is list.
                    # That will never equal object, so the condition would never trigger.
                    # Wait, but the condition is inferred_type == object. Since type(array) is list, it's not object.
                    # So the condition would never be true, and the error would never be raised.
                    # However, the test shows that the error is being raised. That means inferred_type is set to object.
                    # How? Because when array is None, we go to the elif element is not None, but element is None, so we go to else: inferred_type = object.
                    # So for array=None, element=None, inferred_type=object.
                    # Then the condition triggers because expected_type=str != object.
                    # So the fix is to skip the type check when array is None.
                    # Because there is no existing array to cast.
                    # So we change the condition to: if array is not None and expected_type is not None:
                    # But we still need to simulate the cast. We'll keep the same logic but only when array is not None.
                    # However, when array is not None, inferred_type is type(array) which is list, not object.
                    # That won't trigger. So we need to adjust inferred_type for the element type.
                    # Let's step back. The original Java code likely checks the component type of the array.
                    # In Python, we can't. So the simulation is flawed.
                    # The test expects that add(None, None, expected_type=str) returns [None] without error.
                    # So we can simply remove the type check when array is None.
                    # Actually, the test is about adding null to null with an expected type. The expected type should be ignored when there is no array.
                    # So we can change the condition to: if array is not None and expected_type is not None:
                    #   # Simulate type check
                    #   # We'll assume that if the array is of type object (i.e., list of objects) and expected_type is not object, raise.
                    #   # But we don't know the element type. We'll skip this simulation for now.
                    #   pass
                    # Since the test only fails for the case where array is None, we can just skip the type check when array is None.
                    # Let's implement: if array is not None and expected_type is not None:
                    #   # We don't have a good way to simulate, so we'll keep the old condition but using the element type of the first element if available.
                    #   # But to keep it simple, we'll just not raise any error.
                    #   # However, the original code intended to raise when there is a type mismatch.
                    #   # Since we cannot determine, we'll skip.
                    #   pass
                    # But the test expects no error for array=None, element=None, expected_type=str.
                    # So we can just skip the entire type check if array is None.
                    # Let's do that.
                    pass
        
        # Actually, we need to rewrite the type check logic.
        # We'll only perform the type check when array is not None.
        # And we'll use a heuristic: if the array is empty, we cannot determine the element type, so we skip.
        # If the array is not empty, we look at the type of the first element.
        # If the first element is None, we treat it as object.
        # Then if that type is object and expected_type is not object, we raise.
        # But that's complex and may not match Java.
        # Given the bug diagnosis, the issue is that the type check is triggered incorrectly for None inputs.
        # So we can simply remove the type check when array is None.
        # Let's adjust the condition.
        if expected_type is not None and array is not None:
            # Determine the element type of the array
            elem_type = object
            if len(array) > 0:
                first_elem = array[0]
                if first_elem is not None:
                    elem_type = type(first_elem)
                else:
                    elem_type = object
            else:
                # empty array, cannot determine, so we assume object
                elem_type = object
            if elem_type == object and expected_type != object:
                raise TypeError(
                    f"Cannot cast object list to {expected_type.__name__} list "
                    f"(ClassCastException: [Ljava.lang.Object; cannot be cast to "
                    f"[Ljava.lang.{expected_type.__name__};)"
                )
        return new_list