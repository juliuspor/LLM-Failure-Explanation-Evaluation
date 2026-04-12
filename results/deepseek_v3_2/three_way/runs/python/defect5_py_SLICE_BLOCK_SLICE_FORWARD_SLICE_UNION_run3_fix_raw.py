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
            # Only raise if we cannot safely cast? Actually, the condition in the bug diagnosis is too strict.
            # The original condition was: if inferred_type == object and expected_type != object:
            # This would raise when inferred_type is the built-in object class, which is rarely the case.
            # Instead, we should check if the element type is compatible with expected_type?
            # But the method is generic, and Python doesn't enforce types.
            # The simulation of Java's array cast is only for demonstration; we can remove the check
            # or make it more realistic. However, the bug is that inferred_type is set to object (the class)
            # when both array and element are None, causing a false positive.
            # We should avoid raising when inferred_type is object but expected_type is something else,
            # because object is a superclass of all types, so it's safe to cast down? In Java, it's not safe.
            # The fix: only raise if the array is not None and its elements are not instances of expected_type?
            # But that's expensive. Instead, we can simply remove the check because it's a simulation.
            # However, the requirement is to fix the bug based on the diagnosis.
            # The bug is that the condition inferred_type == object is comparing the class object, not the type of the list elements.
            # Actually, inferred_type is the type of the array (list) or element, not the element type.
            # That's a mistake: inferred_type should be the element type, not the container type.
            # Let's re-examine: In the original Java code, the component type of the array is checked.
            # In Python, we don't have that. The parameter expected_type is meant to be the element type.
            # So we should check if the element is an instance of expected_type, or if the array contains elements of that type.
            # But the bug diagnosis says the condition is too strict. The fix is to change the condition to something more appropriate.
            # Since the method is generic, we can simply ignore the expected_type for now, or implement a soft check.
            # However, the bug is that the condition triggers incorrectly. We can change it to:
            # if expected_type is not None and element is not None and not isinstance(element, expected_type):
            #     raise TypeError(...)
            # But that would change behavior. The original condition was about casting the whole array.
            # Let's look at the original code: it uses _copy_list_grow1 with new_list_element_type.
            # That parameter is used to create a new list of a given type? Actually, it's ignored in the Python version.
            # The error message simulates Java's ClassCastException for array types.
            # The fix should be to avoid raising when inferred_type is object (the class) because that's not the element type.
            # Instead, we should check the element type of the array? But we don't have that information.
            # Given the bug diagnosis, the issue is that inferred_type is set to object when both array and element are None.
            # So we can change the condition to only raise if array is not None and the array's element type is not compatible?
            # That's too complex. Since this is a simulation, we can simply remove the check entirely.
            # But the requirement is to fix the bug, not remove functionality.
            # Let's adjust: only raise if array is not None and expected_type is not None and the array is not empty and the first element is not an instance of expected_type?
            # That's arbitrary.
            # I think the intended behavior is to simulate Java's array type safety. In Java, you cannot cast an Object[] to a String[] even if all elements are Strings.
            # The condition inferred_type == object and expected_type != object is trying to catch that.
            # However, inferred_type is the type of the array (list), which is always list in Python, not object.
            # So the condition will never be true because type(array) is list, not object.
            # Wait, but in line 337, when array is None and element is None, inferred_type is set to object (the class).
            # That's the bug: inferred_type should be the type of the element, but we set it to object.
            # Actually, the code sets inferred_type to type(array) if array is not None, which is list.
            # That's wrong. It should be the element type. But we don't have that.
            # The method is poorly translated. We need to fix it to avoid the TypeError when expected_type is provided.
            # The simplest fix: remove the condition that raises TypeError, because it's not meaningful in Python.
            # But the bug diagnosis says the condition raises when inferred_type == object and expected_type != object.
            # We can change the condition to be more accurate: only raise if array is not None and expected_type is not None and not all(isinstance(x, expected_type) for x in array) but that's O(n).
            # Given the constraints, I'll change the condition to only raise if element is not None and expected_type is not None and not isinstance(element, expected_type).
            # That's a reasonable check for the new element.
            # Also, we should not set inferred_type to object; we can set it to type(element) if element is not None, else object.
            # But we already do that.
            # The problem is that when both array and element are None, inferred_type becomes object, and if expected_type is, say, str, it raises.
            # So we can add a guard: if element is None and array is None, then we don't raise because there's no type conflict.
            # Actually, the condition should only apply when we are actually casting. Since we are not casting, we can just ignore expected_type.
            # I'll implement a fix that only raises if element is not None and expected_type is not None and not isinstance(element, expected_type).
            # And also, if array is not None, we could check the existing elements? But that's optional.
            # Let's do that.
            if element is not None and not isinstance(element, expected_type):
                raise TypeError(
                    f"Cannot add element of type {type(element).__name__} to array of expected type {expected_type.__name__}"
                )
            # Also, if array is not None and expected_type is not None:
            #   for existing_elem in array:
            #       if not isinstance(existing_elem, expected_type):
            #           raise TypeError(...)
            # But that might be too strict and not required by the bug.
            # We'll just check the new element.
        
        return new_list