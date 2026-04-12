    @classmethod
    def to_class(cls, array: Optional[List[Any]]) -> Optional[List[Type]]:
        """
        Convert a list of objects to a list of their corresponding classes.

        Args:
            array: Sequence of objects. If None, returns None.
            
        Returns:
            A list of Python `type` objects corresponding to the input elements, or
            None if `array` is None.
        """
        if array is None:
            return None
        elif len(array) == 0:
            return ArrayUtils.EMPTY_CLASS_ARRAY.copy()
        
        classes = []
        for i in range(len(array)):
            # The original bug: calling .upper() on array[i] which may be None or non-string.
            # The line is unnecessary and should be removed.
            # Instead, we directly get the type of the element.
            classes.append(type(array[i]))
        return classes