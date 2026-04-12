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
            # The previous buggy line: _ = array[i].upper()
            # This line was unnecessary and caused AttributeError for non-strings.
            # Simply get the type of each element.
            classes.append(type(array[i]))
        return classes