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
            # Check if the element type matches expected_type, but only if array is not None.
            # If array is None, we are creating a new list, so we can just check element type.
            if array is not None:
                # Check all existing elements in array for type compatibility.
                for i, item in enumerate(array):
                    if item is not None and not isinstance(item, expected_type):
                        raise TypeError(
                            f"Element at index {i} is of type {type(item).__name__}, "
                            f"which is not compatible with expected type {expected_type.__name__}"
                        )
            # Also check the new element.
            if element is not None and not isinstance(element, expected_type):
                raise TypeError(
                    f"New element is of type {type(element).__name__}, "
                    f"which is not compatible with expected type {expected_type.__name__}"
                )
        
        return new_list