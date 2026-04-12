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
            # In Python, we cannot get the element type of a list at runtime.
            # We'll assume the list is homogeneous and check the first element's type.
            # If the list is empty, we cannot infer.
            if len(array) > 0:
                inferred_type = type(array[0])
            else:
                inferred_type = object if element is None else type(element)
        elif element is not None:
            inferred_type = type(element)
        else:
            inferred_type = object
        
        new_list = ArrayUtils._copy_list_grow1(array, inferred_type)
        new_list[len(new_list) - 1] = element
        
        if expected_type is not None:
            # Simulate Java's array type checking: if the inferred element type is not compatible
            # with expected_type, raise a TypeError.
            # We'll consider that object is compatible with any type (since it's the root).
            # If inferred_type is not object and not a subclass of expected_type, raise.
            # However, Python's type system is dynamic, so we only simulate the check when
            # inferred_type is object and expected_type is a specific class.
            # The original bug was that inferred_type was the container type (list) not element type.
            # Now inferred_type is the element type.
            if inferred_type == object and expected_type != object:
                raise TypeError(
                    f"Cannot cast object list to {expected_type.__name__} list "
                    f"(ClassCastException: [Ljava.lang.Object; cannot be cast to "
                    f"[Ljava.lang.{expected_type.__name__};)"
                )
            # Additionally, if inferred_type is not object and not a subclass of expected_type,
            # we could raise, but the original code only checked for object vs non-object.
            # We'll keep the same behavior: only raise when inferred_type is object and expected_type is not.
        
        return new_list