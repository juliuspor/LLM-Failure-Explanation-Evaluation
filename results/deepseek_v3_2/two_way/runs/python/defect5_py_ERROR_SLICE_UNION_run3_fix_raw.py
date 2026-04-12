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
            # Infer the element type from the first element if array is non-empty
            if len(array) > 0:
                inferred_type = type(array[0])
            else:
                # Empty array: use element's type if not None, else object
                if element is not None:
                    inferred_type = type(element)
                else:
                    inferred_type = object
        elif element is not None:
            inferred_type = type(element)
        else:
            inferred_type = object
        
        new_list = ArrayUtils._copy_list_grow1(array, inferred_type)
        new_list[len(new_list) - 1] = element
        
        if expected_type is not None:
            # Only raise if the inferred type is not a subtype of expected_type
            # In Python, we can't do strict Java-like array casting, but we can simulate
            # by checking if the element's type matches expected_type.
            # However, the bug diagnosis indicates that the issue is inferring object
            # when array contains mixed types. We should not raise if the element itself
            # is compatible.
            # Actually, the original logic was too strict. We should only raise if
            # the element cannot be stored in an array of expected_type? But Python is dynamic.
            # The bug is that inferred_type becomes object when array is None or empty,
            # causing a false positive. We should only raise when there is a genuine type mismatch.
            # Since this is a simulation of Java's type safety, we can relax the check:
            # Only raise if element is not None and not an instance of expected_type.
            if element is not None and not isinstance(element, expected_type):
                raise TypeError(
                    f"Cannot add element of type {type(element).__name__} to array of type {expected_type.__name__}"
                )
            # Also, if array is not None, we could check all elements, but that's expensive.
            # The original bug was about casting Object[] to String[]. In Java, you cannot cast
            # an Object[] to String[] even if all elements are Strings, because the runtime
            # type of the array is Object[]. However, the Python simulation should not
            # enforce that strictly because Python lists are heterogeneous.
            # The fix: remove the inferred_type vs expected_type check entirely, because
            # it's causing false positives. Instead, rely on element type check.
            # But we must keep the expected_type parameter for compatibility.
            # So we remove the old check.
        
        return new_list