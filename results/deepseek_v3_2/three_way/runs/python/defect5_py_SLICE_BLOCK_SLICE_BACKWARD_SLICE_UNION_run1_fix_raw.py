    @staticmethod
    def add(array: Optional[List[T]], element: T) -> List[T]:
        """
        Return a new list with `element` appended.

        This is a functional-style helper: the input list is not modified. If
        `array` is None, it is treated as an empty list.

        Args:
            array: Source list (may be None).
            element: Element to append.
            
        Returns:
            A new list containing the original elements followed by `element`.
        """
        if array is not None:
            new_list = array.copy()
            new_list.append(element)
            return new_list
        else:
            return [element]