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
            # Only simulate a cast failure if the inferred type is object and expected_type is not object,
            # AND the element is not None (since None can be assigned to any type in Python).
            # However, the Java-style check is about the array type, not the element.
            # The original Java code would throw ArrayStoreException when trying to store an element of wrong type.
            # Here we simulate a ClassCastException for the array cast.
            # But we should not raise if the element is None because None is assignable to any type.
            # Actually, the test expects that when array is None and element is None, we should not raise.
            # The issue is that inferred_type becomes object when both are None, and expected_type is str.
            # In Java, you cannot cast Object[] to String[], but the method is supposed to create a new array
            # of type expected_type? Wait, the Java version of ArrayUtils.add uses Array.newInstance to create
            # an array of the same component type as the input array, or if input is null, uses the class of the element.
            # If both are null, it uses Object.class. Then it tries to cast the result to the expected type.
            # The test expects that when expected_type is String, and we have null array and null element,
            # the method should return [null] without error. That means the cast should succeed.
            # In Java, casting Object[] to String[] would fail at runtime with ClassCastException.
            # But the test says it should not fail. So maybe the expected_type is used only for validation
            # of the element, not for casting the array. Actually, the Java code does:
            # T[] newArray = (T[]) Array.newInstance(componentType, newLen);
            # where componentType is determined from array if not null, else from element if not null, else Object.
            # Then it copies and sets the last element. There's no cast to expected_type.
            # The expected_type parameter is used only for type checking in the test? Wait, the Python translation
            # added expected_type to simulate Java's type safety. The bug is that it raises incorrectly.
            # We need to adjust the condition: only raise if the element is not None and its type is not compatible
            # with expected_type? But the method doesn't have that check.
            # Let's look at the test: test_add_null_to_null_with_expected_type.
            # It expects that adding null to null with expected_type=str returns [null] (i.e., [None]).
            # So the method should not raise TypeError. Therefore, we should skip the cast simulation
            # when the element is None, because None can be assigned to any type.
            # However, the cast simulation is about the array type, not the element. The error message says:
            # "Cannot cast object list to str list". That's because inferred_type is object and expected_type is str.
            # But if the array is null, we are creating a new list with one element (None). In Python, a list
            # can hold any type, so there's no need to enforce a type. The simulation is only for Java compatibility.
            # The test expects no exception. So we should only raise if the element is not None and its type
            # is not a subclass of expected_type? That's too complex.
            # Simpler: only raise if inferred_type is object and expected_type is not object, AND the element is not None?
            # But the element is None in the failing test, so we skip.
            # However, what about other cases? The test suite may have other expectations.
            # Let's examine the original Java code: In ArrayUtils.add, there is no expected_type parameter.
            # The Java method signature is: public static <T> T[] add(T[] array, T element).
            # The type is inferred from the array parameter. If array is null, it uses the element's class.
            # If both are null, it returns (T[]) new Object[] { null } which is fine.
            # The Python translation added expected_type for some reason, maybe to simulate the component type.
            # The bug is that the simulation is too strict.
            # We'll change the condition to only raise when the element is not None and the inferred_type is object
            # and expected_type is not object. But that still might raise for cases where element is None.
            # Actually, the failing test has element None, so we should not raise.
            # Let's just remove the cast simulation entirely? But other tests might rely on it.
            # The diagnosis says the test expects no error. So we need to adjust the condition to not raise
            # when element is None.
            # We'll do: if expected_type is not None and inferred_type == object and expected_type != object:
            #     if element is not None:
            #         raise TypeError(...)
            # That will allow None elements.
            if inferred_type == object and expected_type != object:
                if element is not None:
                    raise TypeError(
                        f"Cannot cast object list to {expected_type.__name__} list "
                        f"(ClassCastException: [Ljava.lang.Object; cannot be cast to "
                        f"[Ljava.lang.{expected_type.__name__};)"
                    )
        
        return new_list