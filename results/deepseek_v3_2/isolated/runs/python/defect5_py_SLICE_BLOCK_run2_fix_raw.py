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
            # Check if the element type matches expected_type
            # If element is not None, check its type
            if element is not None and not isinstance(element, expected_type):
                raise TypeError(
                    f"Cannot add element of type {type(element).__name__} to list of expected type {expected_type.__name__}"
                )
            # Additionally, if array is not None, we could check its elements, but that's expensive.
            # For simplicity, we only check the new element.
            # The Java-style cast simulation is not needed here.
        
        return new_list