    @staticmethod
    def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
        """
        Return a new list with `element` appended.
        This is a functional-style helper: the input list is not modified.
        If `array` is None, it is treated as an empty list.
        """
        if array is not None:
            new_list = array.copy()
        else:
            new_list = []
        new_list.append(element)
        return new_list
