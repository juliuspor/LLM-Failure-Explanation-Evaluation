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
            # In Python, we cannot directly get the element type of a list.
            # We'll assume the list is homogeneous and check the first element if exists.
            if len(array) > 0:
                first_element_type = type(array[0])
            else:
                first_element_type = object if element is None else type(element)
        elif element is not None:
            first_element_type = type(element)
        else:
            first_element_type = object
        
        new_list = ArrayUtils._copy_list_grow1(array, first_element_type)
        new_list[len(new_list) - 1] = element
        
        if expected_type is not None:
            # Simulate Java array cast: if the existing list's element type is not compatible
            # with expected_type, raise TypeError.
            # We'll consider that if first_element_type is not a subclass of expected_type,
            # and expected_type is not object, then we raise.
            # However, since Python lists are heterogeneous, we can only approximate.
            # The original bug was comparing container type to object.
            # We'll change to compare first_element_type to expected_type.
            # But we must also handle the case where array is empty and element is None.
            # We'll follow the original intention: if expected_type is not object and
            # the inferred element type is object (i.e., we have an object list),
            # then raise.
            if first_element_type == object and expected_type != object:
                raise TypeError(
                    f"Cannot cast object list to {expected_type.__name__} list "
                    f"(ClassCastException: [Ljava.lang.Object; cannot be cast to "
                    f"[Ljava.lang.{expected_type.__name__};)"
                )
        
        return new_list