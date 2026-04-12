    @staticmethod
    def add(array: Optional[List[T]], element: T) -> List[T]:
        """
        Return a new list with `element` appended.
        
        Args:
            array: Source list (may be None).
            element: Element to append.
            
        Returns:
            A new list containing the original elements followed by `element`.
        """
        if array is None:
            return [element]
        result = array.copy()
        result.append(element)
        return result