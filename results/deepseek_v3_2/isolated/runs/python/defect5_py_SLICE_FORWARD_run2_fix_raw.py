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
        if array is None:
            array = []
        new_list = array.copy()
        new_list.append(element)
        
        if expected_type is not None:
            # Simulate type checking: if array is empty, we cannot infer type from elements.
            # We'll just check if the element matches expected_type if element is not None.
            if element is not None and not isinstance(element, expected_type):
                raise TypeError(
                    f"Cannot add element of type {type(element).__name__} to list expected to contain {expected_type.__name__}"
                )
        return new_list