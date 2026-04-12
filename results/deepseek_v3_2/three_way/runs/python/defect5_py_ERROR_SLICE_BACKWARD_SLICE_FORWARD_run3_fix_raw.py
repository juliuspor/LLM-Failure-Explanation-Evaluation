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
            if element is not None and not isinstance(element, expected_type):
                raise TypeError(
                    f"Cannot add element of type {type(element).__name__} to an array of type {expected_type.__name__}"
                )
            # Also check existing array elements if array is not None
            if array is not None:
                for i, item in enumerate(array):
                    if item is not None and not isinstance(item, expected_type):
                        raise TypeError(
                            f"Array contains element at index {i} of type {type(item).__name__} which is not compatible with {expected_type.__name__}"
                        )
        
        return new_list