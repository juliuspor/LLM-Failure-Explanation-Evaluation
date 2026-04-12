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
            # Both array and element are None, we cannot infer a concrete type.
            # Use object as default, but skip type checking if expected_type is provided?
            # Actually, the bug is that we raise TypeError when expected_type != object.
            # We should treat this case as valid: adding None to an empty list.
            # So we set inferred_type to object, but we should not raise TypeError
            # if expected_type is not object? The diagnosis says we need to handle
            # the case where both are None appropriately.
            # The issue is that the type check is too strict. In Java, adding null to an array
            # of a specific type is allowed. So we should allow expected_type to be any type,
            # and not raise TypeError just because inferred_type is object.
            # Actually, the error simulation is for Java array cast. If array is None and element is None,
            # we create a list with one None element. That list is of type list[object] essentially.
            # If expected_type is provided and is not object, the Java simulation would fail because
            # you cannot cast Object[] to String[] for example. But in Python, we don't have that restriction.
            # However, the bug is that the function incorrectly raises TypeError when both are None.
            # We need to adjust the condition: only raise TypeError if array is not None and its type
            # is object but expected_type is something else? Actually, the original code's logic is flawed.
            # Let's re-examine: The function is supposed to simulate Java's array addition with type safety.
            # The inferred_type is used to check if we can cast. If array is None, we don't have a concrete
            # array type, so we should not enforce the cast? The bug diagnosis says: when both array and element
            # are None, inferred_type is set to object, and if expected_type is not object, a TypeError is raised.
            # That is undesirable because adding None to an empty list should be allowed regardless of expected_type.
            # So we should skip the type check when array is None and element is None? Or treat inferred_type as expected_type?
            # Actually, the expected_type is provided by the caller to simulate a Java array of that type.
            # If the caller expects a specific type, they should provide an array of that type. If array is None,
            # we are creating a new list. In Java, you cannot create a generic array without knowing the type.
            # But in Python, we can. So to fix the bug, we should only raise TypeError when array is not None
            # and the type of array is object (i.e., a generic object array) but expected_type is a more specific type.
            # However, the current code uses inferred_type = type(array) which returns the class of the array (list).
            # That's not the element type. Wait, look at line 337: inferred_type = type(array). That's wrong!
            # It should be the element type of the array, not the array itself. But the array is a list, so type(array) is list.
            # That's not helpful. Actually, the original Java code would have component type of the array. In Python,
            # we don't have that. So the simulation is flawed. The bug is that type(array) returns list, not the element type.
            # So the condition inferred_type == object will never be true because list != object. That means the TypeError
            # would never be raised? But the bug says it does raise when both are None. Because when array is None and element is None,
            # inferred_type is set to object (line 337). That's because the else clause sets inferred_type = object.
            # So object is a class, not an instance. Then line 343 checks if inferred_type == object and expected_type != object.
            # object is the built-in class object. So if expected_type is, say, str, then condition is true and TypeError is raised.
            # That's the bug. We need to change the logic: the type check should only apply when we have an actual array (not None)
            # and we are trying to simulate a cast. But since we cannot get the element type in Python, maybe we should remove
            # this type check altogether? However, the function is part of a larger library that might rely on this behavior.
            # The bug diagnosis says we need to handle the case where both are None appropriately. So we can simply skip the
            # type check when array is None and element is None. Alternatively, we can set inferred_type to expected_type if
            # expected_type is provided, else object. But that might mask other issues.
            # Let's think: The purpose of expected_type is to simulate Java's type checking. In Java, if you have an Object[]
            # and you try to assign it to a String[] variable, you get a ClassCastException. The Python code is trying to
            # simulate that by checking if inferred_type is object and expected_type is not object. But inferred_type is set
            # to the type of the array (list) or the type of the element. That's not correct. Actually, the Java version
            # would have the component type of the array. In Python, we don't have that, so the simulation is approximate.
            # The bug is that when both are None, we set inferred_type to object, which is a placeholder for generic object array.
            # If expected_type is provided and is not object, we raise TypeError. But that's too strict because we are creating
            # a new list with a None element, which could be of any type. In Java, you can have a String[] array containing null.
            # So the type check should not fail when adding null to an empty array of a specific type.
            # Therefore, we should adjust the condition: only raise TypeError if array is not None and array is actually an
            # object array (how to know?) Since we cannot know, maybe we should remove the type check entirely for this method.
            # But the bug is specific to the case where both array and element are None. So we can fix by not raising TypeError
            # when array is None and element is None. Let's do that: if array is None and element is None, we skip the type check.
            # However, the condition also triggers when array is None but element is not None? In that case, inferred_type is type(element).
            # That might be a specific type, and if expected_type is different, should we raise? Probably not, because we are creating
            # a new list with that element type. The simulation is messy.
            # Given the bug diagnosis, the fix should be to handle the case where both array and element are None by not raising
            # TypeError. We can achieve that by checking if array is None and element is None, then set inferred_type to expected_type
            # if expected_type is not None, else object. But that might be overcomplicating.
            # Simpler: remove the type check altogether. But the function might be used in tests that expect the TypeError.
            # Let's look at the original code: the type check is only for simulating Java's ClassCastException. It's not essential
            # for Python functionality. We can keep it but fix the logic: only raise if array is not None and the array's element type
            # is object? Since we don't have element type, we can't. So maybe we should just remove the type check from this method.
            # However, the bug is in the add method, and we are only allowed to fix that method. We cannot change other parts.
            # So we need to adjust the condition to avoid the false positive when both are None.
            # Let's change the condition: only raise TypeError if array is not None and inferred_type == object and expected_type != object.
            # But inferred_type is type(array) which is list, not object. So that condition will never be true. Wait, the else clause sets
            # inferred_type = object. So when array is None and element is None, inferred_type is object. That's the case we want to avoid.
            # So we can add an extra condition: if array is None and element is None, then skip the type check.
            # Let's implement that.
            inferred_type = object
        
        new_list = ArrayUtils._copy_list_grow1(array, inferred_type)
        new_list[len(new_list) - 1] = element
        
        if expected_type is not None:
            # Skip type check when both array and element are None, because we cannot infer a concrete type
            # and adding None to an empty list should be allowed for any expected type.
            if array is None and element is None:
                pass
            elif inferred_type == object and expected_type != object:
                raise TypeError(
                    f"Cannot cast object list to {expected_type.__name__} list "
                    f"(ClassCastException: [Ljava.lang.Object; cannot be cast to "
                    f"[Ljava.lang.{expected_type.__name__};)"
                )
        
        return new_list